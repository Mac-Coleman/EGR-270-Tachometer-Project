import time
import RPi.GPIO as GPIO
import smbus
from enum import Enum

class TachometerState(Enum):
    SPLASH_SCREEN = 0
    MENU_OPTIONS = 1
    MEASURE_FREQUENCY = 2
    INPUT_FREQUENCY = 3

state = TachometerState.SPLASH_SCREEN

bus = smbus.SMBus(1)
keyboard_address = 0x30

def check_input():
    # Test whether any inputs are being held.
    # Returns character being held or None.
    key = bus.read_byte_data(keyboard_address, 0)
    # Read the byte 0 (the key being pressed.)

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

def flash():
    global STROBE_TRIGGER
    GPIO.output(STROBE_TRIGGER, GPIO.LOW)
    GPIO.output(STROBE_TRIGGER, GPIO.HIGH)

def calculate_rpm():
    global time_diff # Time difference in nanoseconds.
    t = time_diff * 1000000000 # time difference in seconds
    t *= 50 # Period of rotation
    f = 1/t # Angular frequency
    r = f * 60 # Rotations per minute
    return r


time_diff = 0

def photogate_callback(channel):
    global count, last_time, time_diff
    count += 1
    count %= 50
    if count == 0:
        flash()
    t = time.time_ns()
    time_diff = t - last_time # Calculate time difference in nanoseconds.

# Initialize everything
PHOTOGATE_GPIO = 22
STROBE_TRIGGER = 6
count = 0
last_time = time.time_ns()
frequency = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PHOTOGATE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(STROBE_TRIGGER, GPIO.OUT)
GPIO.output(STROBE_TRIGGER, GPIO.HIGH)

GPIO.add_event_detect(PHOTOGATE_GPIO, GPIO.FALLING, callback=photogate_callback)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()

while True:
    if state == TachometerState.SPLASH_SCREEN:
        print("Testing Splash Screen")
        time.sleep(2)
        state = TachometerState.MENU_OPTIONS

    elif state == TachometerState.MENU_OPTIONS:
        print("Testing Menu Options")

        choice = wait_for_input()
        if choice == "1":
            state = TachometerState.MEASURE_FREQUENCY
        elif choice == "2":
            state = TachometerState.INPUT_FREQUENCY

    elif state == TachometerState.MEASURE_FREQUENCY:
        if debounced_check() == "*":
            state = TachometerState.INPUT_FREQUENCY

        print(str(calculate_rpm) + " RPM")
        time.sleep(1)
        print("Measuring Frequency!")

    elif state == TachometerState.INPUT_FREQUENCY:
        if debounced_check() == "*":
            state = TachometerState.MEASURE_FREQUENCY
        print("Exact Frequency")

