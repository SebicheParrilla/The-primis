from machine import Pin
import time

# Optical sensor on GP1
sensor = Pin(1, Pin.IN)

counter = 0
last_state = sensor.value()

# Time of the previous count
last_count_time = time.ticks_us()

print("Optical sensor counter started")

while True:
    current_state = sensor.value()

    # Detect LOW -> HIGH
    if last_state == 0 and current_state == 1:
        counter += 1

        # Calculate elapsed time since previous count
        current_time = time.ticks_us()
        elapsed = time.ticks_diff(current_time, last_count_time)

        print("Count:", counter, " | Time since last:", elapsed, "us")

        last_count_time = current_time

    last_state = current_state

    time.sleep_us(100)