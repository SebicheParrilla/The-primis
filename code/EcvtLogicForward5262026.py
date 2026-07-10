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

# =========================================================
# TARGET CARRIER / TRANSMISSION OUTPUT SPEED
# =========================================================

TARGET_CARRIER_RPM = 70

# =========================================================
# POWER SETTINGS
# =========================================================

# M2 simulates pneumatic engine.
# It stays fixed. The program reads actual flywheel RPM.
M2_POWER_PERCENT = 70
M2_DUTY = int(65535 * (M2_POWER_PERCENT / 100))

# M1 was too weak before, so raise minimum active power.
M1_MIN_ACTIVE_PERCENT = 25
M1_MIN_ACTIVE_DUTY = int(65535 * (M1_MIN_ACTIVE_PERCENT / 100))

# Start M1 stronger so carrier estimate can climb.
M1_START_PERCENT = 40
m1_duty = int(65535 * (M1_START_PERCENT / 100))

MIN_DUTY = 0
MAX_DUTY = 65535

# =========================================================
# CONTROL SETTINGS
# =========================================================

# Stronger correction because carrier estimate was stuck at 40-50.
M1_KP = 24
MAX_DUTY_STEP = 1200
MIN_CORRECTION_STEP = 250

RPM_DEADBAND = 3
CONTROL_INTERVAL_MS = 150

RPM_SMOOTHING = 0.20
PWM_SMOOTHING = 0.60

last_control_ms = time.ticks_ms()

# =========================================================
# DIRECTION SETTINGS
# =========================================================

# M2 direction from your working setup
M2_FORWARD = False

# M1 should ADD speed for driving.
# If M1 Power rises but Carrier Est does not rise, flip this to False.
M1_FORWARD = True

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
# STARTUP
# =========================================================

print("Starting active carrier-speed control in 3 seconds...")
time.sleep(3)

print("==============================================")
print("eCVT ACTIVE CARRIER SPEED CONTROL")
print("M2 fixed power:", M2_POWER_PERCENT, "%")
print("Target carrier/output RPM:", TARGET_CARRIER_RPM)
print("M1 start power:", M1_START_PERCENT, "%")
print("M1 min active power:", M1_MIN_ACTIVE_PERCENT, "%")
print("==============================================")

run_motor(m2_a, m2_b, M2_DUTY, M2_FORWARD)
run_motor(m1_a, m1_b, m1_duty, M1_FORWARD)

# =========================================================
# MAIN LOOP
# =========================================================

try:
    while True:
        now_us = time.ticks_us()
        now_ms = time.ticks_ms()

        # =================================================
        # READ M1 ENCODER RPM
        # =================================================

        motor_rpm = calc_rpm(motor_intervals, MOTOR_PULSES_PER_REV)

        if motor_rpm is None:
            motor_rpm = motor_last_rpm

        motor_last_rpm = apply_stop(
            motor_last_time,
            now_us,
            MOTOR_STOP_TIMEOUT_US,
            motor_rpm
        )

        # Actual M1 gearbox output RPM
        motor_output_rpm = motor_last_rpm / GEAR_RATIO

        # =================================================
        # READ FLYWHEEL ENCODER RPM
        # =================================================

        fly_rpm = calc_rpm(flywheel_intervals, FLYWHEEL_PULSES_PER_REV)

        if fly_rpm is None:
            fly_rpm = flywheel_last_rpm

        flywheel_last_rpm = apply_stop(
            flywheel_last_time,
            now_us,
            FLYWHEEL_STOP_TIMEOUT_US,
            fly_rpm
        )

        # =================================================
        # SMOOTH BOTH RPM VALUES
        # =================================================

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

        # =================================================
        # LIVE eCVT CALCULATION
        # =================================================

        # Carrier/output estimate using live sensor values:
        # carrier = ((1.4 * flywheel) + (2.5 * m1_output)) / 6

        estimated_carrier_rpm = (
            (1.4 * smooth_flywheel_rpm) +
            (2.5 * smooth_motor_output_rpm)
        ) / 6

        # Required M1 output RPM using live flywheel RPM:
        # target_m1 = ((6 * target_carrier) - (1.4 * flywheel)) / 2.5

        target_m1_output_rpm = (
            (6 * TARGET_CARRIER_RPM) -
            (1.4 * smooth_flywheel_rpm)
        ) / 2.5

        if target_m1_output_rpm < 0:
            target_m1_output_rpm = 0

        m1_error = target_m1_output_rpm - smooth_motor_output_rpm

        # =================================================
        # M1 CONTROL
        # =================================================

        if time.ticks_diff(now_ms, last_control_ms) >= CONTROL_INTERVAL_MS:
            last_control_ms = now_ms

            if abs(m1_error) > RPM_DEADBAND:
                m1_change = m1_error * M1_KP
                m1_change = apply_min_correction(m1_change)
                m1_change = limit_step(m1_change, MAX_DUTY_STEP)

                target_duty = m1_duty + m1_change
                target_duty = clamp(target_duty, MIN_DUTY, MAX_DUTY)
                target_duty = apply_min_active_duty(target_duty)

                m1_duty = smooth_value(m1_duty, target_duty, PWM_SMOOTHING)
                m1_duty = clamp(m1_duty, MIN_DUTY, MAX_DUTY)
                m1_duty = apply_min_active_duty(m1_duty)

                run_motor(m1_a, m1_b, m1_duty, M1_FORWARD)

        m1_power_percent = (m1_duty / 65535) * 100

        print(
            "Carrier Target:",
            TARGET_CARRIER_RPM,
            "| Carrier Est:",
            round(estimated_carrier_rpm, 1),
            "| Fly:",
            round(smooth_flywheel_rpm, 1),
            "| M1 Target:",
            round(target_m1_output_rpm, 1),
            "| M1 Out:",
            round(smooth_motor_output_rpm, 1),
            "| Err:",
            round(m1_error, 1),
            "| M1 Power:",
            round(m1_power_percent, 1),
            "%"
        )

        time.sleep(0.1)

finally:
    motor_stop(m1_a, m1_b)
    motor_stop(m2_a, m2_b)

    print("MOTORS STOPPED")