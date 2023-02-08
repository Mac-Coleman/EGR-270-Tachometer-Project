import smbus
import math
import RPi.GPIO as GPIO
import signal
import sys

bus = smbus.SMBus(1)
keyboard_address = 0x30
switch_address = 0x20
pwm_output = 26

def check_input():
    key = bus.read_byte_data(keyboard_address, 0)

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
    global last_char
    k = check_input()

    while k == None or k == last_char:
        last_char = k
        k = check_input()

    last_char = k

    return k

def input_prompt():

    output_string = ""

    cancel = 0
    while True:
        k = wait_for_input()

        if k == "#":
            print()
            break
        if k == "*":
            cancel += 1
            output_string += "."
        else:
            output_string += k

        print("\r" + output_string, end="      ")

        if cancel >= 2:
            print()
            return None

    return float(output_string)

def set_rpm(num):
    global rpm, pwm
    frequency = num / 60
    pwm_frequency = frequency * 50
    pwm_frequency = math.floor(pwm_frequency)
    if pwm_frequency > 8000:
        print("Too high!")
        return
    
    if pwm_frequency < 10:
        print("Too low!")
        return
    
    pwm.ChangeFrequency(pwm_frequency)
    pwm.start(50)
    frequency = pwm_frequency / 50
    rpm = frequency * 60

def setup():
    bus.write_byte(0x20, 1)
    # Make sure bit 0 is high to switch to s2

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

rpm = None
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_output, GPIO.OUT)
pwm = GPIO.PWM(pwm_output, 5)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    setup()
    
    print("Please enter your RPM")
    
    num = input_prompt()
    
    if num != None:
        set_rpm(num)
        print("RPM Set: " + str(rpm))
    else:
        print("Canceled.")

signal.pause()