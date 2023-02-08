# Trying it again, from the top this time.
# Writing I/O will be done exclusively over I2C.
# No GPIO writes at all. Requires one GPIO input for detecting pulses, but that's it.

from enum import Enum
import time
import smbus
import RPi.GPIO as GPIO
import signal
import sys

class TachometerState(Enum):
    SPLASH_SCREEN = 0
    MENU_OPTIONS = 1
    MEASURE_FREQUENCY = 2
    INPUT_FREQUENCY = 3


def read(adr, byte):
    return bus.read_byte_data(adr, byte)

def check_input():
    # Test whether any inputs are being held.
    # Returns character being held or None.
    # Read the byte 0 (the key being pressed.)

    key = read(KEYBOARD_ADDRESS, 0)
    c = None
    if key != 0:
        c = chr(key)

    return c

last_char = None

def debounced_check():
    global last_char

    k = check_input()
    if k == last_char:
        last_char = k
        k = check_input()
        return None

    last_char = k
    return k

def wait_for_input():
    # Blocking wait for any inputs to be given. Will wait until a key is pressed.
    # Always returns a character, never None, after some delay.

    global last_char

    k = check_input()

    while k == None or k == last_char:
        last_char = k
        k = check_input()

    last_char = k

    return k

def interrupt_signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)
    
def calculate_rpm():
    global time_diff # Time difference in nanoseconds.
    t = time_diff / 1000000000 # time difference in seconds
    t *= 50 # Period of rotation
    f = 1/t # Angular frequency
    r = f * 60 # Rotations per minute
    return r

time_diff = sys.maxsize

def photogate_callback(channel):
    global last_time, time_diff
    t = time.time_ns()
    time_diff = t - last_time # Calculate time difference in nanoseconds.
    last_time = t

# Initialize everything
KEYBOARD_ADDRESS = 0x30
bus = smbus.SMBus(1)
PHOTOGATE_GPIO = 27
count = 0
last_time = time.time_ns()
frequency = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PHOTOGATE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(PHOTOGATE_GPIO, GPIO.FALLING, callback=photogate_callback)

signal.signal(signal.SIGINT, interrupt_signal_handler)

state = TachometerState.SPLASH_SCREEN

while True:
    if state == TachometerState.SPLASH_SCREEN:
        print("Welcome!")
        time.sleep(2)
        state = TachometerState.MENU_OPTIONS
    elif state == TachometerState.MENU_OPTIONS:
        print("Menu: 1) Measure 2) Input")

        i = wait_for_input()

        if i == '1':
            state = TachometerState.MEASURE_FREQUENCY
            print("Measure Frequency")
        elif i == '2':
            state = TachometerState.INPUT_FREQUENCY
            print("Input Frequency")
    elif state == TachometerState.MEASURE_FREQUENCY:
        print("\r" + str(calculate_rpm()) + "RPM                  ", end='')
        time.sleep(1)

        k = debounced_check()
        if k == '*':
            state = TachometerState.INPUT_FREQUENCY
    else:
        GPIO.cleanup()
        sys.exit(0)
