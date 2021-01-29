import RPi.GPIO as GPIO

def button_callback(channel):
    print("Button was pushed!")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#while True:
#    if GPIO.input(3) == GPIO.HIGH:
#        print("Button was pushed")

GPIO.add_event_detect(3,GPIO.RISING,callback=button_callback)
message = input("Waiting for button....\nPress enter to quit\n\n")

GPIO.cleanup()
