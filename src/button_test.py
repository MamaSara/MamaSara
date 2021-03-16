import signal
import sys
import RPi.GPIO as GPIO

def signal_handler(sig, frame):
    print("\nCleaning up ...")
    GPIO.cleanup()
    print("Bye")
    sys.exit(0)
    return

def button_callback(self):
    print("Button pressed")
    return

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
        GPIO.add_event_detect(3, GPIO.RISING, callback=button_callback)
        print("Press button")
        input()

