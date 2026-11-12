from machine import Pin, PWM, UART, I2C
from bno08x import *
from i2c import BNO08X_I2C
from led import *
import time


# ============================================================
# LED
# ============================================================

# HIGH = OFF
# LOW  = ON

led_positive = Pin(10, Pin.OUT)
led_negative = Pin(11, Pin.OUT)
led_positive.value(1)
led_negative.value(0)

SOLENOID = Pin(
    3,
    Pin.OUT
)

SOLENOID.value(1)

led("red")


# ============================================================
# UART TO RASPBERRY PI
# ============================================================

uart_pi = UART(
    0,
    tx=16,
    rx=17,
    baudrate=115200,
    timeout=2
)


# ============================================================
# URM37
# ============================================================

uart_sensor = UART(
    1,
    tx=4,
    rx=5,
    baudrate=9600,
    timeout=2
)


# ============================================================
# BNO085
# ============================================================

i2c1 = I2C(
    1,
    scl=Pin(27),
    sda=Pin(26),
    freq=100_000
)

int_pin = Pin(19, Pin.IN, Pin.PULL_UP)
reset_pin = Pin(18, Pin.OUT)

bno = BNO08X_I2C(
    i2c1,
    address=0x4A,
    int_pin=int_pin,
    reset_pin=reset_pin,
    debug=False
)

bno.quaternion.enable(20)


# ============================================================
# VALUES
# ============================================================

yaw = 0
raw_yaw = 0.0
yaw_offset = 0.0
distance = 0

startr = 0
servo_angle = 0

# THIS IS NOW THE 1-7 MODE COMMAND
speed_mode = 3

program_started = False


# ============================================================
# START BUTTON
# ============================================================

start_button = Pin(
    20,
    Pin.IN,
    Pin.PULL_UP
)


# ============================================================
# SERVO
# ============================================================

servo = PWM(Pin(2))
servo.freq(50)


# ============================================================
# ELECTRIC MOTOR
# ============================================================

MOTOR_A = PWM(Pin(8))
MOTOR_B = PWM(Pin(9))

MOTOR_A.freq(1000)
MOTOR_B.freq(1000)


# ============================================================
# ELECTRIC MOTOR ENCODER
# ============================================================

enc_a = Pin(
    7,
    Pin.IN,
    Pin.PULL_UP
)

enc_b = Pin(
    6,
    Pin.IN,
    Pin.PULL_UP
)

COUNTS_PER_REV = 356.4

motor_count = 0
motor_armed = False


def update_motor_encoder():

    global motor_count
    global motor_armed

    a = enc_a.value()
    b = enc_b.value()

    state = (a << 1) | b

    # 00 arms the next count
    if state == 0:

        motor_armed = True

    # 11 after 00 = one count
    elif state == 3 and motor_armed:

        motor_count += 1
        motor_armed = False


# ============================================================
# FLYWHEEL OPTICAL ENCODER
# ============================================================

sensor = Pin(
    1,
    Pin.IN
)

SLOTS = 16
TIMEOUT_US = 100000

flywheel_count = 0

flywheel_last_state = sensor.value()

flywheel_last_count_time = time.ticks_us()

flywheel_intervals = []


def add_flywheel_sample(value):

    flywheel_intervals.append(value)

    if len(flywheel_intervals) > 7:

        flywheel_intervals.pop(0)


def update_flywheel_encoder():

    global flywheel_count
    global flywheel_last_state
    global flywheel_last_count_time

    current_time = time.ticks_us()

    current_state = sensor.value()


    # LOW -> HIGH
    if (
        flywheel_last_state == 0
        and current_state == 1
    ):

        elapsed = time.ticks_diff(
            current_time,
            flywheel_last_count_time
        )

        flywheel_count += 1

        flywheel_last_count_time = current_time

        add_flywheel_sample(elapsed)


    # Timeout
    if time.ticks_diff(
        current_time,
        flywheel_last_count_time
    ) >= TIMEOUT_US:

        add_flywheel_sample(0)

        flywheel_last_count_time = current_time


    flywheel_last_state = current_state


def get_flywheel_rpm():

    if not flywheel_intervals:

        return 0


    # Flywheel stopped
    if flywheel_intervals[-1] == 0:

        return 0


    valid_samples = [
        x for x in flywheel_intervals
        if x > 0
    ]


    if not valid_samples:

        return 0


    average = sum(valid_samples) / len(valid_samples)


    rpm = (
        60000000 /
        (average * SLOTS)
    )


    return rpm




# ============================================================
# MOTOR CONTROL
# ============================================================

# YOUR ACTUAL MOTOR WIRING
#
# FORWARD:
# GP8 = LOW
# GP9 = PWM
#
# REVERSE:
# GP8 = PWM
# GP9 = LOW


def stop_motor():

    MOTOR_A.duty_u16(0)
    MOTOR_B.duty_u16(0)


def forward(percent):

    percent = max(
        0,
        min(100, percent)
    )

    pwm = int(
        percent * 65535 / 100
    )

    MOTOR_A.duty_u16(0)

    MOTOR_B.duty_u16(pwm)


def reverse(percent):

    percent = max(
        0,
        min(100, percent)
    )

    pwm = int(
        percent * 65535 / 100
    )

    MOTOR_A.duty_u16(pwm)

    MOTOR_B.duty_u16(0)


# ============================================================
# MOTOR DIRECTION
# ============================================================

# +1 = forward
# -1 = reverse
#  0 = stopped

motor_direction = 0


# ============================================================
# EXECUTE MODE
# ============================================================

def set_mode(mode):

    global motor_direction


    # --------------------------------------------------------
    # MODE 1
    # HIGH SPEED REVERSE
    # PNEUMATIC OFF
    # --------------------------------------------------------

    if mode == 1:

#         print("MODE 1: HIGH REVERSE")

        motor_direction = -1

        SOLENOID.value(1)

        reverse(100)


    # --------------------------------------------------------
    # MODE 2
    # LOW SPEED REVERSE
    # PNEUMATIC OFF
    # --------------------------------------------------------

    elif mode == 2:

#         print("MODE 2: LOW REVERSE")

        motor_direction = -1

        SOLENOID.value(1)

        reverse(50)


    # --------------------------------------------------------
    # MODE 3
    # STOP
    # --------------------------------------------------------

    elif mode == 3:

#         print("MODE 3: STOP")

        motor_direction = 0

        stop_motor()

        SOLENOID.value(1)


    # --------------------------------------------------------
    # MODE 4
    # LOW SPEED FORWARD
    # PNEUMATIC OFF
    # --------------------------------------------------------

    elif mode == 4:

#         print("MODE 4: LOW FORWARD")

        motor_direction = 1

        SOLENOID.value(1)

        forward(50)


    # --------------------------------------------------------
    # MODE 5
    # LOW FORWARD + PNEUMATIC
    # --------------------------------------------------------

    elif mode == 5:

#         print("MODE 5: LOW FORWARD + PNEUMATIC")

        motor_direction = 1

        SOLENOID.value(0)

        forward(50)


    # --------------------------------------------------------
    # MODE 6
    # MEDIUM FORWARD + PNEUMATIC
    # --------------------------------------------------------

    elif mode == 6:

#         print("MODE 6: MEDIUM FORWARD + PNEUMATIC")

        motor_direction = 1

        SOLENOID.value(0)

        forward(70)


    # --------------------------------------------------------
    # MODE 7
    # HIGH FORWARD + PNEUMATIC
    # --------------------------------------------------------

    elif mode == 7:

#         print("MODE 7: HIGH FORWARD + PNEUMATIC")

        motor_direction = 1

        SOLENOID.value(0)

        forward(100)


# ============================================================
# RECEIVE FROM RASPBERRY PI
# ============================================================

def receive_pi():

    global startr
    global servo_angle
    global speed_mode


    if not uart_pi.any():

        return


    data = uart_pi.read()


    if data is None:

        return


    try:

        message = data.decode(
            "utf-8",
            "ignore"
        )


        print(
            message,
            end=""
        )


        messages = message.split("\n")


        for msg in messages:

            msg = msg.strip()


            if not msg:

                continue


            parts = msg.split(",")


            if len(parts) >= 3:

                startr = int(
                    float(parts[0])
                )

                servo_angle = int(
                    float(parts[1])
                )

                new_mode = int(
                    float(parts[2])
                )


                # Only accept valid modes
                if 1 <= new_mode <= 7:

                    speed_mode = new_mode

                    set_mode(
                        speed_mode
                    )


    except Exception as e:

        print(
            "UART ERROR:",
            e
        )


# ============================================================
# STEERING
# ============================================================

def steering(angle):

    angle = max(
        -50,
        min(50, angle)
    )


    pulse = int(
        1500000 +
        angle * 10000
    )


    pulse = max(
        1000000,
        min(2000000, pulse)
    )


    servo.duty_ns(
        pulse
    )


# ============================================================
# SEND SENSOR DATA TO PI
# ============================================================

def send_sensor_data():

    message = (
        str(
            1 if program_started else 0
        )
        + ","
        + "{:.2f}".format(yaw)
        + ","
        + str(distance)
        + "\n"
    )


    uart_pi.write(
        message.encode("utf-8")
    )


# ============================================================
# RPM TIMING
# ============================================================

last_rpm_time = time.ticks_ms()

last_motor_count = 0


# ============================================================
# URM37 TIMING
# ============================================================

last_distance = time.ticks_ms()


# ============================================================
# START
# ============================================================

stop_motor()

SOLENOID.value(1)

steering(0)


# print()
# print("==============================")
# print("     AIZA MOTOR CONTROLLER")
# print("==============================")
# print()
# 
# print("1 = HIGH REVERSE")
# print("2 = LOW REVERSE")
# print("3 = STOP")
# print("4 = LOW FORWARD")
# print("5 = LOW FORWARD + PNEUMATIC")
# print("6 = MEDIUM FORWARD + PNEUMATIC")
# print("7 = HIGH FORWARD + PNEUMATIC")

# print()

set_mode(3)


# ============================================================
# MAIN LOOP
# ============================================================

while True:


    # ========================================================
    # IMU
    # ========================================================

    bno.update_sensors()


    if bno.quaternion.updated:

        raw_yaw, pitch, roll = (
            bno.quaternion.euler
        )


        yaw = (
            raw_yaw -
            yaw_offset
        )


        if yaw > 180:

            yaw -= 360


        elif yaw < -180:

            yaw += 360


    # ========================================================
    # RECEIVE PI COMMAND
    # ========================================================

    receive_pi()


    # ========================================================
    # STEERING
    # ========================================================

    steering(
        servo_angle
    )


    # ========================================================
    # START BUTTON
    # ========================================================

    if (
        startr == 1
        and not program_started
    ):

        led("green")


        if start_button.value() == 0:

            yaw_offset = raw_yaw

            yaw = 0.0

            program_started = True

            print(
                "STARTED — YAW ZEROED"
            )
            led("yellow")


    # ========================================================
    # SEND SENSOR DATA
    # ========================================================

    if startr == 1:

        send_sensor_data()



    # ========================================================
    # ENCODERS
    # ========================================================

    update_motor_encoder()

    update_flywheel_encoder()


    # ========================================================
    # RPM EVERY 500 ms
    # ========================================================

    now = time.ticks_ms()


    if time.ticks_diff(
        now,
        last_rpm_time
    ) >= 500:


        elapsed = time.ticks_diff(
            now,
            last_rpm_time
        )


        # ----------------------------------------------------
        # ELECTRIC MOTOR RPM
        # ----------------------------------------------------

        motor_counts = (
            motor_count -
            last_motor_count
        )


        motor_revolutions = (
            motor_counts /
            COUNTS_PER_REV
        )


        motor_rpm = (
            motor_revolutions *
            60000 /
            elapsed
        )


        # Direction
        if motor_direction < 0:

            motor_rpm = -motor_rpm


        elif motor_direction == 0:

            motor_rpm = 0


        # ----------------------------------------------------
        # FLYWHEEL RPM
        # ----------------------------------------------------

        flywheel_rpm = (
            get_flywheel_rpm()
        )


        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

#         print(
#             "MODE: {} | "
#             "MOTOR: {:7.1f} RPM | "
#             "FLYWHEEL: {:7.1f} RPM".format(
#                 speed_mode,
#                 motor_rpm,
#                 flywheel_rpm
#             )
#         )


        last_motor_count = motor_count

        last_rpm_time = now


    # ========================================================
    # URM37
    # ========================================================

    if time.ticks_diff(
        now,
        last_distance
    ) >= 150:


        last_distance = now


        uart_sensor.write(
            bytes([
                0x22,
                0x00,
                0x00,
                0x22
            ])
        )


        time.sleep_ms(50)


        data = uart_sensor.read()


        if data and len(data) >= 4:


            for i in range(
                len(data) - 3
            ):


                if data[i] != 0x22:

                    continue


                high = data[i + 1]

                low = data[i + 2]

                checksum = data[i + 3]


                calculated = (
                    0x22 +
                    high +
                    low
                ) & 0xFF


                if checksum == calculated:


                    distance = (
                        (high << 8) |
                        low
                    )


                    break


    time.sleep_ms(10)