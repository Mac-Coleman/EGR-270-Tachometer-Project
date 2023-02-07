import RPi.GPIO as GPIO
import time
import signal
import sys

SPOKE_GPIO = 22
STROBE_TRIGGER = 6
count = 0
last_time = time.time_ns()
frequency = 0

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

def spoke_callback(channel):
    global count, last_time, frequency
    t = time.time_ns()
    count += 1
    count %= 50
    if count == 0:
        print("Flash!")
        GPIO.output(STROBE_TRIGGER, GPIO.LOW)
        GPIO.output(STROBE_TRIGGER, GPIO.HIGH)
        #flash strobe

    p = (t - last_time) / 1000000000
    frequency = 1 / (p * 50)
    print(str(frequency) + " Hz")
    print(t - last_time)
    last_time = t


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SPOKE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(STROBE_TRIGGER, GPIO.OUT)
    GPIO.output(STROBE_TRIGGER, GPIO.HIGH)

    GPIO.add_event_detect(SPOKE_GPIO, GPIO.FALLING, callback=spoke_callback)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
