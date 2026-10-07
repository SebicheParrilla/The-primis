from machine import Pin
import time

# Optical sensor
sensor = Pin(1, Pin.IN)

counter = 0
last_state = sensor.value()
last_count_time = time.ticks_us()

# Rolling queue of 7 intervals
intervals = []

print("Optical sensor started")

while True:
    current_state = sensor.value()

    # Detect LOW -> HIGH
    if last_state == 0 and current_state == 1:

        current_time = time.ticks_us()

        # Time since previous count
        elapsed = time.ticks_diff(current_time, last_count_time)

        counter += 1
        last_count_time = current_time

        # Add new interval
        intervals.append(elapsed)

        # Remove oldest if more than 7
        if len(intervals) > 7:
            intervals.pop(0)

        # Print the 7 values currently being kept
        print("Count:", counter)
        print("Intervals:", intervals)

    last_state = current_state

    time.sleep_us(100)