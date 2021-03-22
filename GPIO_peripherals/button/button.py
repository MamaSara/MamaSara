# use pin 4 for button.
# may need to change input_device_index in recorder.py
import RPi.GPIO as GPIO
from datetime import datetime
from recorder import Recorder
GPIO.setmode(GPIO.BOARD)

#GPIO pin of component
class record_audio_button(object):
    def __init__(self, filename, button_pin):
        self.filename = filename
        self.button_pin = button_pin
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.rec = Recorder(channels=1)

    def release_button(self, channel):
        print("Button released, stoping recording....")
        GPIO.remove_event_detect(self.button_pin)
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback=self.press_button, bouncetime=10)
        self.recfile.stop_recording()
        self.recfile.close()

    def press_button(self, channel):
        print("Button pressed, recording.....")
        GPIO.remove_event_detect(self.button_pin)
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self.release_button, bouncetime=10)
        self.recfile = self.rec.open(self.filename + str(datetime.now())+'.wav', 'wb')
        self.recfile.start_recording()

    def start(self):
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback=self.press_button, bouncetime=10)

rec = record_audio_button('request', 3)
rec.start()

try:
    input("Waiting for button to be pressed....\nPress Enter to quit\n")

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
