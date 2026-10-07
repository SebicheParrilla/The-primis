from machine import Pin, UART
from time import sleep_ms
from led import *

led("green")

# UART to Raspberry Pi (same wiring style as HuskyLens but separate UART)
uart_pi = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

counter = 0

while True:
    message = "MOTION_DATA:" + str(counter) + "\n"
    uart_pi.write(message)

    counter += 1
    sleep_ms(500)
    led("red")