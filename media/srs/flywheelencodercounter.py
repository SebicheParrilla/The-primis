from machine import Pin
import time

# Optical sensor
sensor = Pin(4, Pin.IN, Pin.PULL_UP)

# Counter
counter = 0

# Previous sensor state
last_state = sensor.value()

print("Optical sensor counter started")

while True:
    current_state = sensor.value()

    # Detect HIGH -> LOW
    if last_state == 1 and current_state == 0:
        counter += 1
        print("Count:", counter)

    last_state = current_state

    time.sleep_us(100)
    =