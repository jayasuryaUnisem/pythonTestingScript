import RPi.GPIO as gpio
import time

pin1 = 2
pin2 = 3


gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(pin1, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(pin2, gpio.IN, pull_up_down = gpio.PUD_DOWN)

while 1:
    print("Pin 1 Value = ",gpio.input(pin1), ", pin 2 Value = ", gpio.input(pin2))
    time.sleep(1)