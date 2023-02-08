import RPi.GPIO as GPIO
import time
import smbus
import signal
import sys

PHOTOGATE_GPIO = 17
last_time = time.time_ns()
frequency = 0

def signal_handler(signal, frame):
    GPIO.cleanup()
    print("")
    sys.exit(0)
    
def setup():
        # Have to write "0" to make "in". Connects s1 (2) to d(1)
        bus.write_byte(0x20, 0)

def spoke_callback(channel):
    global count, last_time, frequency
    t = time.time_ns()
    p = (t - last_time) / 1000000000
    frequency = 1 / (p * 50)
    print("\r" + str(frequency * 60) + " RPM                           ", end="")
    last_time = t


if __name__ == "__main__":
    print("Measuring RPM:")
    bus = smbus.SMBus(1)
    setup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PHOTOGATE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(PHOTOGATE_GPIO, GPIO.FALLING, callback=spoke_callback)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()