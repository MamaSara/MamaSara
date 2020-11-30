# use pin 4 for button.
# may need to change input_device_index in recorder.py
import RPi.GPIO as GPIO
from datetime import datetime
from recorder import Recorder
GPIO.setmode(GPIO.BCM)

#GPIO pin of component
class record_audio_button(object):
    def __init__(self, filename, button_pin):
        self.filename = filename
        self.button_pin = button_pin
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.rec = Recorder(channels=1)

    def release_button(self, channel):
        GPIO.remove_event_detect(self.button_pin)
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self.press_button, bouncetime=10)
        self.recfile.stop_recording()
        self.recfile.close()

    def press_button(self, channel):
        GPIO.remove_event_detect(self.button_pin)
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback=self.release_button, bouncetime=10)
        self.recfile = self.rec.open(self.filename + str(datetime.now())+'.wav', 'wb')
        self.recfile.start_recording()

    def start(self):
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self.press_button, bouncetime=10)

rec = record_audio_button('test', 4)
rec.start()

try:
    input()

except KeyboardInterrupt:
    gpio.cleanup()
gpio.cleanup()