from machine import Pin
import time

PULSES_PER_REV = 9
GEAR_RATIO = 39.6

# timeout (adjust later if needed)
TIMEOUT_US = 200000  # 0.2 seconds

intervals = [0, 0, 0, 0, 0]

last_time = 0
last_pulse_time = 0
armed = True

def irq(pin):
    global last_time, last_pulse_time, armed, intervals

    state = pin.value()
    now = time.ticks_us()

    # re-arm when signal goes HIGH
    if state == 1:
        armed = True
        return

    # valid pulse (LOW edge)
    if state == 0 and armed:
        armed = False
        last_pulse_time = now

        if last_time != 0:
            dt = time.ticks_diff(now, last_time)

            # shift buffer (3-sample middle averaging system)
            intervals[0] = intervals[1]
            intervals[1] = intervals[2]
            intervals[2] = intervals[3]
            intervals[3] = intervals[4]
            intervals[4] = dt

        last_time = now


sensor = Pin(6, Pin.IN, Pin.PULL_UP)
sensor.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=irq)


def get_motor_rpm():
    if intervals[2] == 0:
        return 0

    mid = (intervals[1] + intervals[2] + intervals[3]) / 3
    if mid == 0:
        return 0

    return (60 * 1000000) / (mid * PULSES_PER_REV)


def get_output_rpm():
    return get_motor_rpm() / GEAR_RATIO


while True:
    now = time.ticks_us()

    # ⛔ timeout: no pulses = motor stopped
    if time.ticks_diff(now, last_pulse_time) > TIMEOUT_US:
        rpm = 0
    else:
        rpm = get_output_rpm()

    print(rpm)
    time.sleep(0.1)