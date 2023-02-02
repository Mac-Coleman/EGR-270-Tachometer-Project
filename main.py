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

def wait_for_input():
    # Blocking wait for any inputs to be given. Will wait until a key is pressed.
    # Always returns a character, never None, after some delay.

    k = check_input()

    while k == None:
        time.sleep(0.025)
        k = check_input()

    return k


while True:
    if state == TachometerState.SPLASH_SCREEN:
        print("Testing Splash Screen")
        time.sleep(0.5)
        state = TachometerState.MENU_OPTIONS
    elif state == TachometerState.MENU_OPTIONS:
        print("Testing Menu Options")
        print(wait_for_input())
        state = TachometerState.MEASURE_FREQUENCY
    # elif state == TachometerState.MEASURE_FREQUENCY:
        # print("Measuring Frequency")
    elif state == TachometerState.INPUT_FREQUENCY:
        print("Exact Frequency")
