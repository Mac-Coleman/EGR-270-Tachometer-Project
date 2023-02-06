import time
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
        print("Measuring Frequency!")

    elif state == TachometerState.INPUT_FREQUENCY:
        if debounced_check() == "*":
            state = TachometerState.MEASURE_FREQUENCY
        print("Exact Frequency")

