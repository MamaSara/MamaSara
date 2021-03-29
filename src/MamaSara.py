'''
Working attempt with button integrated
Using event based trigger
'''
import signal
import sys
import requests
import subprocess
import time
import RPi.GPIO as GPIO
import gpiozero
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Setup GPIO peripherals with gpiozero
button = gpiozero.Button(6)
shutdown_button = gpiozero.Button(3)
manual_stop_button = gpiozero.Button(4)
red_LED = gpiozero.PWMLED(17)
green_LED = gpiozero.PWMLED(27)
blue_LED = gpiozero.PWMLED(22)

# Setup LCD with digitalio
lcd_rs = digitalio.DigitalInOut(board.D13)
lcd_en = digitalio.DigitalInOut(board.D21)
lcd_d4 = digitalio.DigitalInOut(board.D19)
lcd_d5 = digitalio.DigitalInOut(board.D16)
lcd_d6 = digitalio.DigitalInOut(board.D26)
lcd_d7 = digitalio.DigitalInOut(board.D20)
lcd_coloumns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_coloumns, lcd_rows)

# Define function to handle interrupt signal
def signal_handler(sig, frame):
    lcd.clear()
    lcd.message = "Cleaning up..."
    print("Cleaning up ...")
    leds_off()
    subprocess.call("docker stop rasa_actions rasa_server micvad > /dev/null 2>&1", shell=True)
    subprocess.call("docer rm rasa_actions rasa_server > /dev/null 2>&1", shell=True)
    lcd.clear()
    lcd.message = "Bye!"
    print("Bye!")
    time.sleep(2)
    lcd.clear()
    sys.exit(0)
    return

def exitMamaSara():
    lcd.clear()
    lcd.message = "Cleaning up..."
    print("Cleaning up ...")
    leds_off()
    subprocess.call("docker stop rasa_actions rasa_server micvad > /dev/null 2>&1", shell=True)
    subprocess.call("docker rm rasa_actions rasa_server > /dev/null 2>&1", shell=True)
    lcd.clear()
    lcd.message = "Bye!"
    print("Bye!")
    time.sleep(2)
    lcd.clear()
    sys.exit(0)

def shutdown():
    lcd.clear()
    lcd.message = "Cleaning up..."
    print("Cleaning up...")
    leds_off()
    subprocess.call("docker stop rasa_actions rasa_server micvad > /dev/null 2>&1", shell=True)
    subprocess.call("docker rm rasa_actions rasa_server > /dev/null 2>&1", shell=True)
    lcd.clear()
    lcd.message = "Going to sleep.."
    print("Going to sleep")
    time.sleep(2)
    lcd.clear()
    subprocess.call(['shutdown', '-h', 'now'], shell=False)

def red_led_on(value):
    red_LED.value = value
    green_LED.value = 0
    blue_LED.value = 0

def green_led_on(value):
    red_LED.value = 0
    green_LED.value = value
    blue_LED.value = 0

def blue_led_on(value):
    red_LED.value = 0
    green_LED.value = 0
    blue_LED.value = value

def leds_off():
    red_LED.value = 0
    green_LED.value = 0
    blue_LED.value = 0

def conversation_event():
    # STT portion of pipeline
    lcd.clear()
    lcd.message = "Go ahead"
    print("Go ahead")
    red_led_on(0.5)
    subprocess.call("docker exec -it micvad bash -c \"python3 mvs_single.py -v 1 -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer --rate 44100\" > /dev/null 2>&1", shell=True)
    subprocess.call("docker cp micvad:/dspeech/results.txt /home/pi/MamaSara/micvadstreaming/results.txt", shell=True)
    print("\nMamaSara V2 thinks you said:")
    user_msg_file = open("/home/pi/MamaSara/micvadstreaming/results.txt", "r")
    user_msg = user_msg_file.read()
    user_msg_file.close()
    stt_end = time.time()
    print(user_msg)
        
    blue_led_on(0.5)
    lcd.clear()
    lcd.message = "Processing..."
    nlp_start = time.time()
    # NLP Portion of pipeline
    response = requests.post('http://localhost:5005/webhooks/rest/webhook',json={"sender": "test", "message": user_msg})

    # TTS Portion of pipeline
    tts_start = time.time()
    response_file = open("/home/pi/MamaSara/rasa/response.txt", "w+")
    response_txt = ""
    for i in response.json():
        print(i['text'])
        response_file.write(i['text'])
        response_txt = response_txt + i['text']
    print("\n")

    audio = subprocess.Popen(['espeak', '-ven-us+f3', response_txt, '--stdout'], stdout=subprocess.PIPE)
    tts_end = time.time()
    aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
    audio.wait()
    aplay.wait()

    lcd.clear()
    lcd.message = "Press the small\nbutton to speak"
    print("Press the small button to speak")

if __name__ == "__main__":
    blue_led_on(0.5)
    lcd.clear()
    lcd.message = "Booting up..."
    print("Booting up...")
    manual_stop_button.when_pressed = exitMamaSara
    shutdown_button.when_pressed = shutdown
    # SIGINT Handler setup
    signal.signal(signal.SIGINT, signal_handler)

    # Start Rasa actions container
    subprocess.call("docker-compose run -d --rm --name rasa_actions rasa run actions > /dev/null 2>&1", shell=True)

    # Start Rasa server container
    subprocess.call("docker-compose run -d -p 5005:5005 --rm --name rasa_server rasa run -m models --endpoints endpoints.yml > /dev/null 2>&1", shell=True)
    # Wait for one second, enough time for the rasa server to be up and running
    time.sleep(45)

    # Start DeepSpeech container
    subprocess.call("docker run -t -d --rm -w /dspeech --name micvad --device /dev/snd:/dev/snd cwrogers1/mamasara-deepspeech:micvad > /dev/null 2>&1", shell=True)
    subprocess.call("docker cp /home/pi/MamaSara/micvadstreaming/mvs_single.py micvad:./dspeech/mvs_single.py", shell=True)
    print("Boot up complete.")

    # Mama Sara Introduction
    green_led_on(0.5)
    lcd.clear()
    lcd.message = "Hello. How can I\nhelp?"
    intro = "Hello. How can I help?"
    audio = subprocess.Popen(['espeak', '-ven-us+f3', intro, '--stdout'], stdout=subprocess.PIPE)
    aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
    audio.wait()
    aplay.wait()

    lcd.clear()
    lcd.message = "Press the small\nbutton to speak"
    print("Press the small\nbutton to speak")
    while True:
        button.wait_for_release()
        conversation_event()
        green_led_on(0.5)

    lcd.clear()
    lcd.message = "Bye!"
    print("Cleaning up...")
    leds_off()
    subprocess.call("docker stop rasa_actions rasa_server micvad > /dev/null 2>&1", shell=True)
    subprocess.call("docker rm  rasa_actions rasa_server > /dev/null 2>&1", shell=True)
    print("Bye")
