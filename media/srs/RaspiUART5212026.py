import serial
import time

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)

print("Listening to Motion...\n")

while True:
    data = ser.readline().decode(errors='ignore').strip()

    if data:
        print("FROM MOTION →", data)