from machine import Pin
import time

# Optical sensor
sensor = Pin(1, Pin.IN)

counter = 0
last_state = sensor.value()
last_count_time = time.ticks_us()

# Rolling queue of 7 intervals
intervals = []

# Time with no sensor pulse before inserting 0
TIMEOUT_US = 500000

# Encoder disc
SLOTS = 16


def add_sample(value):
    intervals.append(value)

    # Keep only 7 samples
    if len(intervals) > 7:
        intervals.pop(0)


print("Optical sensor started")

while True:
    current_time = time.ticks_us()
    current_state = sensor.value()

    # Detect LOW -> HIGH
    if last_state == 0 and current_state == 1:

        elapsed = time.ticks_diff(current_time, last_count_time)

        counter += 1
        last_count_time = current_time

        add_sample(elapsed)

        average = sum(intervals) / len(intervals)

        if average > 0:
            rpm = 60000000 / (average * SLOTS)
        else:
            rpm = 0

        print("RPM:", rpm)

    # Check for timeout
    if time.ticks_diff(current_time, last_count_time) >= TIMEOUT_US:

        add_sample(0)

        # Reset timer so we don't continuously add zeros
        last_count_time = current_time

        average = sum(intervals) / len(intervals)

        if average > 0:
            rpm = 60000000 / (average * SLOTS)
        else:
            rpm = 0

        print("RPM:", rpm)

    last_state = current_state

    time.sleep_us(100)