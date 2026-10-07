from machine import Pin, PWM
import time

# =========================================================
# MOTOR DRIVER
# =========================================================

# M1 = TRANSMISSION MOTOR
# GP8 = A
# GP9 = B
m1_a = PWM(Pin(8))
m1_b = PWM(Pin(9))

# M2 = PNEUMATIC ENGINE SIMULATOR
# GP10 = A
# GP11 = B
m2_a = PWM(Pin(10))
m2_b = PWM(Pin(11))

PWM_FREQ = 1000

m1_a.freq(PWM_FREQ)
m1_b.freq(PWM_FREQ)

m2_a.freq(PWM_FREQ)
m2_b.freq(PWM_FREQ)

m1_a.duty_u16(0)
m1_b.duty_u16(0)

m2_a.duty_u16(0)
m2_b.duty_u16(0)

# =========================================================
# CONFIG
# =========================================================

MOTOR_PULSES_PER_REV = 9
FLYWHEEL_PULSES_PER_REV = 16
GEAR_RATIO = 39.6

MOTOR_STOP_TIMEOUT_US = 170000
FLYWHEEL_STOP_TIMEOUT_US = 380000

NEUTRAL_RATIO = 0.56
NEUTRAL_TRIM = -22

# =========================================================
# TIMING SETTINGS
# =========================================================

NEUTRAL_TIME_MS = 10000
FULL_SPEED_TIME_MS = 5000

# =========================================================
# POWER SETTINGS
# =========================================================

M2_POWER_PERCENT = 70
M2_DUTY = int(65535 * (M2_POWER_PERCENT / 100))

M1_MIN_ACTIVE_PERCENT = 20
M1_MIN_ACTIVE_DUTY = int(65535 * (M1_MIN_ACTIVE_PERCENT / 100))

M1_FULL_DUTY = 65535

m1_duty = M1_MIN_ACTIVE_DUTY

MIN_DUTY = 0
MAX_DUTY = 65535

# =========================================================
# CONTROL SETTINGS
# =========================================================

M1_KP = 14
MAX_DUTY_STEP = 95
MIN_CORRECTION_STEP = 65
RPM_DEADBAND = 7
CONTROL_INTERVAL_MS = 200

RPM_SMOOTHING = 0.18
PWM_SMOOTHING = 0.25

last_control_ms = time.ticks_ms()

# =========================================================
# DIRECTION SETTINGS
# =========================================================

# M2 was flipped in your working setup
M2_FORWARD = False

# Neutral: M1 opposes flywheel to cancel carrier movement
M1_NEUTRAL_FORWARD = False

# Full speed: M1 spins the other direction to add speed
M1_FULL_FORWARD = True

# =========================================================
# ENCODERS
# =========================================================

motor_intervals = [0, 0, 0, 0, 0]
flywheel_intervals = [0, 0, 0, 0, 0]

motor_last_time = 0
flywheel_last_time = 0

motor_last_rpm = 0
flywheel_last_rpm = 0

smooth_motor_output_rpm = 0
smooth_flywheel_rpm = 0

motor_armed = True
flywheel_armed = True

# =========================================================
# MOTOR CONTROL FUNCTIONS
# =========================================================

def motor_forward(a, b, duty):
    a.duty_u16(int(duty))
    b.duty_u16(0)


def motor_reverse(a, b, duty):
    a.duty_u16(0)
    b.duty_u16(int(duty))


def motor_stop(a, b):
    a.duty_u16(0)
    b.duty_u16(0)


def run_motor(a, b, duty, forward=True):
    duty = int(duty)

    if duty < 0:
        duty = 0

    if duty > 65535:
        duty = 65535

    if forward:
        motor_forward(a, b, duty)
    else:
        motor_reverse(a, b, duty)


def clamp(value, low, high):
    if value < low:
        return low

    if value > high:
        return high

    return value


def limit_step(change, max_step):
    if change > max_step:
        return max_step

    if change < -max_step:
        return -max_step

    return change


def smooth_value(old_value, new_value, amount):
    return old_value + ((new_value - old_value) * amount)


def apply_min_active_duty(duty):
    if duty > 0 and duty < M1_MIN_ACTIVE_DUTY:
        return M1_MIN_ACTIVE_DUTY

    return duty


def apply_min_correction(change):
    if change > 0 and change < MIN_CORRECTION_STEP:
        return MIN_CORRECTION_STEP

    if change < 0 and change > -MIN_CORRECTION_STEP:
        return -MIN_CORRECTION_STEP

    return change

# =========================================================
# IRQ MOTOR ENCODER
# =========================================================

def motor_irq(pin):
    global motor_last_time, motor_armed, motor_intervals

    now = time.ticks_us()
    state = pin.value()

    if state == 1:
        motor_armed = True
        return

    if state == 0 and motor_armed:
        motor_armed = False

        if motor_last_time != 0:
            dt = time.ticks_diff(now, motor_last_time)
            motor_intervals.pop(0)
            motor_intervals.append(dt)

        motor_last_time = now


motor_sensor = Pin(6, Pin.IN, Pin.PULL_UP)
motor_sensor.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=motor_irq)

# =========================================================
# IRQ FLYWHEEL ENCODER
# =========================================================

def flywheel_irq(pin):
    global flywheel_last_time, flywheel_armed, flywheel_intervals

    now = time.ticks_us()
    state = pin.value()

    if state == 1:
        flywheel_armed = True
        return

    if state == 0 and flywheel_armed:
        flywheel_armed = False

        if flywheel_last_time != 0:
            dt = time.ticks_diff(now, flywheel_last_time)
            flywheel_intervals.pop(0)
            flywheel_intervals.append(dt)

        flywheel_last_time = now


flywheel_sensor = Pin(2, Pin.IN, Pin.PULL_UP)
flywheel_sensor.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=flywheel_irq)

# =========================================================
# RPM CALC MEDIAN FILTER
# =========================================================

def calc_rpm(intervals, ppr):
    valid = [x for x in intervals if 200 < x < 200000]

    if len(valid) == 0:
        return None

    valid.sort()
    median = valid[len(valid) // 2]

    return (60 * 1000000) / (median * ppr)

# =========================================================
# STOP HANDLER
# =========================================================

def apply_stop(last_time, now, timeout, last_rpm):
    if last_time != 0:
        if time.ticks_diff(now, last_time) > timeout:
            return 0

    return last_rpm

# =========================================================
# RPM UPDATE FUNCTION
# =========================================================

def update_rpm_values():
    global motor_last_rpm, flywheel_last_rpm
    global smooth_motor_output_rpm, smooth_flywheel_rpm

    now_us = time.ticks_us()

    motor_rpm = calc_rpm(motor_intervals, MOTOR_PULSES_PER_REV)

    if motor_rpm is None:
        motor_rpm = motor_last_rpm

    motor_last_rpm = apply_stop(
        motor_last_time,
        now_us,
        MOTOR_STOP_TIMEOUT_US,
        motor_rpm
    )

    motor_output_rpm = motor_last_rpm / GEAR_RATIO

    fly_rpm = calc_rpm(flywheel_intervals, FLYWHEEL_PULSES_PER_REV)

    if fly_rpm is None:
        fly_rpm = flywheel_last_rpm

    flywheel_last_rpm = apply_stop(
        flywheel_last_time,
        now_us,
        FLYWHEEL_STOP_TIMEOUT_US,
        fly_rpm
    )

    smooth_motor_output_rpm = smooth_value(
        smooth_motor_output_rpm,
        motor_output_rpm,
        RPM_SMOOTHING
    )

    smooth_flywheel_rpm = smooth_value(
        smooth_flywheel_rpm,
        flywheel_last_rpm,
        RPM_SMOOTHING
    )

# =========================================================
# NEUTRAL CONTROL FUNCTION
# =========================================================

def hold_neutral_for(duration_ms):
    global m1_duty, last_control_ms

    start_ms = time.ticks_ms()

    # IMPORTANT FIX:
    # Reset correction timer when neutral starts.
    last_control_ms = time.ticks_ms()

    print("----- MODE: NEUTRAL -----")

    while time.ticks_diff(time.ticks_ms(), start_ms) < duration_ms:
        now_ms = time.ticks_ms()

        update_rpm_values()

        target_motor_output_rpm = (smooth_flywheel_rpm * NEUTRAL_RATIO) + NEUTRAL_TRIM
        neutral_error = target_motor_output_rpm - smooth_motor_output_rpm

        estimated_carrier_rpm = (
            (1.4 * smooth_flywheel_rpm) -
            (2.5 * smooth_motor_output_rpm)
        ) / 6

        if time.ticks_diff(now_ms, last_control_ms) >= CONTROL_INTERVAL_MS:
            last_control_ms = now_ms

            target_duty = m1_duty

            if abs(neutral_error) > RPM_DEADBAND:
                m1_change = neutral_error * M1_KP
                m1_change = apply_min_correction(m1_change)
                m1_change = limit_step(m1_change, MAX_DUTY_STEP)

                target_duty = m1_duty + m1_change

            target_duty = clamp(target_duty, MIN_DUTY, MAX_DUTY)
            target_duty = apply_min_active_duty(target_duty)

            m1_duty = smooth_value(m1_duty, target_duty, PWM_SMOOTHING)

            m1_duty = clamp(m1_duty, MIN_DUTY, MAX_DUTY)
            m1_duty = apply_min_active_duty(m1_duty)

            run_motor(m1_a, m1_b, m1_duty, M1_NEUTRAL_FORWARD)

        m1_power_percent = (m1_duty / 65535) * 100

        print(
            "Mode: NEUTRAL",
            "| Fly:",
            round(smooth_flywheel_rpm, 1),
            "| Target M1:",
            round(target_motor_output_rpm, 1),
            "| M1 Out:",
            round(smooth_motor_output_rpm, 1),
            "| Error:",
            round(neutral_error, 1),
            "| M1 Power:",
            round(m1_power_percent, 1),
            "%",
            "| Carrier Est:",
            round(estimated_carrier_rpm, 1)
        )

        time.sleep(0.1)

# =========================================================
# FULL SPEED FUNCTION
# =========================================================

def full_speed_for(duration_ms):
    global m1_duty

    start_ms = time.ticks_ms()

    print("----- MODE: FULL SPEED -----")

    m1_duty = M1_FULL_DUTY
    run_motor(m1_a, m1_b, m1_duty, M1_FULL_FORWARD)

    while time.ticks_diff(time.ticks_ms(), start_ms) < duration_ms:
        update_rpm_values()

        print(
            "Mode: FULL",
            "| Fly:",
            round(smooth_flywheel_rpm, 1),
            "| M1 Out:",
            round(smooth_motor_output_rpm, 1),
            "| M1 Power: 100.0 %",
            "| Direction: ADDING SPEED"
        )

        time.sleep(0.1)

# =========================================================
# STARTUP
# =========================================================

print("Starting in 3 seconds...")
time.sleep(3)

print("eCVT Neutral Then Full Speed Then Stop")
print("M2 fixed power:", M2_POWER_PERCENT, "%")
print("Neutral time:", NEUTRAL_TIME_MS / 1000, "seconds")
print("Full speed time:", FULL_SPEED_TIME_MS / 1000, "seconds")
print("RPM deadband:", RPM_DEADBAND)
print("Neutral trim:", NEUTRAL_TRIM, "RPM")
print("====================================================")

run_motor(m2_a, m2_b, M2_DUTY, M2_FORWARD)

m1_duty = M1_MIN_ACTIVE_DUTY
run_motor(m1_a, m1_b, m1_duty, M1_NEUTRAL_FORWARD)

try:
    hold_neutral_for(NEUTRAL_TIME_MS)

    full_speed_for(FULL_SPEED_TIME_MS)

finally:
    motor_stop(m1_a, m1_b)
    motor_stop(m2_a, m2_b)

    print("MOTORS STOPPED")