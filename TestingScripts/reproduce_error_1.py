import RPi.GPIO as GPIO
from smbus2 import SMBus
import signal
import sys
import time

PHOTOGATE_GPIO = 17
bus = SMBus(1)
lt = time.time_ns()
count = 0

def event_callback(channel):
    global lt, count
    count += 1
    count %= 50
    if count == 0:
        print("Hey!")
    print("Called")
    t = time.time_ns()
    print(t - lt)
    lt = t

def read():
    print(bus.read_byte_data(0x30, 0))

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PHOTOGATE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(PHOTOGATE_GPIO, GPIO.FALLING, callback=event_callback)

signal.signal(signal.SIGINT, signal_handler)

while True:
    read()
