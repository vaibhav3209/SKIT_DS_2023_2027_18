"""
MODULE 4: RASPBERRY PI TRAFFIC SIGNAL LED DEMO
Purpose: Control one red, yellow and green LED using Raspberry Pi GPIO.

Run this file ON A RASPBERRY PI:
    python traffic_signal.py

Wiring:
- Red LED    -> BCM GPIO 17 (through a suitable resistor)
- Yellow LED -> BCM GPIO 27 (through a suitable resistor)
- Green LED  -> BCM GPIO 22 (through a suitable resistor)

This is a one-direction learning demo, not the complete four-way controller.
Press Ctrl+C to stop. The LEDs are switched off during cleanup.
"""

from gpiozero import LED
from time import sleep

# Create LED objects using BCM GPIO pin numbers.
red = LED(17)
yellow = LED(27)
green = LED(22)

try:
    while True:

        # RED: vehicles must stop.
        red.on()
        yellow.off()
        green.off()
        print("RED - STOP")
        sleep(5)

        # GREEN: vehicles may move.
        red.off()
        yellow.off()
        green.on()
        print("GREEN - GO")
        sleep(10)

        # YELLOW: prepare to stop.
        red.off()
        yellow.on()
        green.off()
        print("YELLOW - WAIT")
        sleep(3)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    # Turn off all LEDs and release GPIO resources.
    red.off()
    yellow.off()
    green.off()

    red.close()
    yellow.close()
    green.close()
