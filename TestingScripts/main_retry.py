import RPi.GPIO as GPIO
import smbus
import signal
import sys
import time
from enum import Enum

class TachometerState(Enum):
    SPLASH_SCREEN = 0
    MENU_OPTIONS = 1
    MEASURE_FREQUENCY = 2
    INPUT_FREQUENCY = 3

def event_callback(channel):
    global lt, count, time_difference
    count = (count + 1) % 50
    t = time.time_ns()
    
    if count == 0:
        flash()
        print("Flash!")
    time_difference = t - lt
    lt = t

def flash():
    print("F")
    GPIO.output(STROBE_TRIGGER, GPIO.LOW)
    print("L")
    GPIO.output(STROBE_TRIGGER, GPIO.HIGH)
    print("H")

def read():
    print(bus.read_byte_data(0x30, 0))

def check_input():
    print("READ")
    key = bus.read_byte_data(keyboard_address, 0)
    print("FINISHED READ")

    c = None
    if key != 0:
        c = chr(key)

    return c

def debounced_check():
    global last_char

    k = check_input()
    if k == last_char:
        last_char = k
        return None

    last_char = k
    return k

def wait_for_input():
    global last_char
    k = check_input()

    while k == None or k == last_char:
        last_char = k
        k = check_input()

    last_char = k

    return k

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)


state = TachometerState.SPLASH_SCREEN
PHOTOGATE_GPIO = 22
STROBE_TRIGGER = 6
keyboard_address = 0x30
bus = smbus.SMBus(1)

lt = time.time_ns()
count = 0
time_difference = sys.maxsize

GPIO.setmode(GPIO.BCM)
GPIO.setup(PHOTOGATE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(STROBE_TRIGGER, GPIO.OUT)

GPIO.add_event_detect(PHOTOGATE_GPIO, GPIO.FALLING, callback=event_callback)

signal.signal(signal.SIGINT, signal_handler)

try:
    while True:

        if state == TachometerState.SPLASH_SCREEN:
            print("Loading")
            time.sleep(1)
            state = TachometerState.MENU_OPTIONS
        elif state == TachometerState.MENU_OPTIONS:
            print("Menu options")

            k = wait_for_input()

            if k == '1':
                state = TachometerState.MEASURE_FREQUENCY
            elif k == '2':
                state = TachometerState.INPUT_FREQUENCY

        elif state == TachometerState.MEASURE_FREQUENCY:
            print("Measure frequency")
            time.sleep(1)
        elif state == TachometerState.INPUT_FREQUENCY:
            print("Input frequency")
            time.sleep(1)
except Exception as e:
    print(str(e))
    GPIO.cleanup()
    sys.exit(0)
