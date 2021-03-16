'''
Attempt one at getting button working with rest of pipeline, micvadstreaming incorporated
Trying to use event based trigger for button, where it interrupts the program and executes a callback function
'''
import requests
import subprocess
import time
import RPi.GPIO as GPIO

def conversation_event_button_callback(self):
    # STT Portion of Event
    subprocess.call("docker exec --interactive --tty --privileged micvad bash -c \"python3 mvs_single.py -v 1 -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer --rate 44100 > /dev/null 2&1\"", shell=True)
    subprocess.call("docker cp micvad:/dspeech/results.txt ../micvadstreaming/results.txt", shell=True)
    print("\nLooking up results for:")
    user_msg_file = open("../micvadstreaming/results.txt", "r")
    user_msg = user_msg_file.read()
    user_msg_file.close()
    print(user_msg)

    # NLP Portion of Event
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": "test", "message": user_msg})

    # TTS Portion of Event
    response_file = open("../rasa/response.txt", "w+")
    response_txt = ""
    for i in response.json():
        print(i['text'])
        response_file.write(i['text'])
        response_txt = response_txt + i['text']
    print("\n")

    audio = subprocess.Popen(['espeak', response_txt, '--stdout'], stdout=subprocess.PIPE)
    aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
    audio.wait()
    aplay.wait()

if __name__ == "__main__":
    # GPIO Setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

    # Mama Sara Introduction
    intro = "Hello. How can I help?"
    audio = subprocess.Popen(['espeak', intro,'--stdout'], stdout=subprocess.PIPE)
    aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
    audio.wait()
    aplay.wait()

    # Start DeepSpeech container
    subprocess.call("docker run --tty --detach --workdir /dspeech --name micvad --device /dev/snd:/dev/snd --privileged=true cwrogers1/mamasara-deepspeech:micvad", shell=True)
    subprocess.call("docker cp ../micvadstreaming/mvs_single.py micvad:./dspeech/mvs_single.py", shell=True)
    user_msg = ''
    while (user_msg.strip() != "goodbye" or user_msg.strip() != "good bye"):
        # Button integration, add event detection and wait for input
        GPIO.add_event_detect(3, GPIO.RISING, callback=conversation_event_button_callback)
        message = input("Press the button to ask me a question\n")
        GPIO.cleanup()
    subprocess.call("docker stop micvad", shell=True)
    subprocess.call("docker rm micvad", shell=True)
