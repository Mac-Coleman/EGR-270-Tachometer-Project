import RPi.GPIO as GPIO
import smbus
import signal
import sys
import time
import threading
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
    time_difference = t - lt
    lt = t

def flash():
    lock.acquire()
    GPIO.output(STROBE_TRIGGER, GPIO.LOW)
    lock.release()
    GPIO.output(STROBE_TRIGGER, GPIO.HIGH)

def read():
    print(bus.read_byte_data(0x30, 0))

def locking_read_i2c_THREAD(address, byte):
    global I2C_READ_BYTE_GLOBAL
    lock.acquire()
    I2C_READ_BYTE_GLOBAL = bus.read_byte_data(address, byte)
    lock.release()

def read_i2c(address, byte):
    t = threading.Thread(target=locking_read_i2c_THREAD, args=(address, byte), daemon=True)
    t.start()
    t.join()

    return I2C_READ_BYTE_GLOBAL

def check_input():
    # key = read_i2c(keyboard_address, 0)
    t = threading.Thread(target=locking_read_i2c_THREAD, args=(keyboard_address, 0), daemon=True)
    t.start()
    t.join()

    key = I2C_READ_BYTE_GLOBAL

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

I2C_READ_BYTE_GLOBAL = 0
last_char = None

state = TachometerState.SPLASH_SCREEN
PHOTOGATE_GPIO = 22
STROBE_TRIGGER = 6
keyboard_address = 0x30
bus = smbus.SMBus(1)

lock = threading.Lock() # The talking stick.

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

            k = debounced_check()
            print(I2C_READ_BYTE_GLOBAL)
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

        time.sleep(0.2)
except Exception as e:
    print(str(e))
    GPIO.cleanup()
    sys.exit(0)
