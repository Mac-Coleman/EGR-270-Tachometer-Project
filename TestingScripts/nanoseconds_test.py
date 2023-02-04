# coding=<utf-8>

import time
import RPi.GPIO as GPIO


C_GPIO = 22

if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(C_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
        print("Awaiting commands")
        GPIO.wait_for_edge(C_GPIO, GPIO.RISING)
        t1 = time.time_ns()

        GPIO.wait_for_edge(C_GPIO, GPIO.RISING)
        t2 = time.time_ns()
        print("Time elapsed: " + str(t2-t1) + " ns")
        print("            : " + str((t2 - t1) / 1000) + " μs")
        print("   Frequency: " + str(1/((t2-t1) / 1000000000)) + " Hz")
        print("         RPM: " + str(((1/((t2 - t1) / 1000000000)) / 50) * 60) + " RPM")
