import RPi.GPIO as GPIO

C_GPIO = 22

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(C_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
        print("State " + str(GPIO.input(C_GPIO)))
