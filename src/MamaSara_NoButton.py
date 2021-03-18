'''
Main MamaSara script without using button, for testing when a button is not available
'''
import signal
import sys
import requests
import subprocess
import time
import RPi.GPIO as GPIO

# Define function to handle interrupt signal
def signal_handler(sig, frame):
    print("\nCleaning up....")
    subprocess.call("docker stop rasa_actions rasa_server micvad > /dev/null 2>&1", shell=True)
    subprocess.call("docker rm rasa_actions rasa_server > /dev/null 2>&1", shell=True)
    print("Bye")
    sys.exit(0)
    return

def conversation_event():
    # STT portion of pipeline
    print("Go ahead")
    subprocess.call("docker exec -it micvad bash -c \"python3 mvs_single.py -v 1 -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer --rate 44100\" > /dev/null 2>&1", shell=True)
    subprocess.call("docker cp micvad:/dspeech/results.txt ../micvadstreaming/results.txt", shell=True)
    print("\nMamaSara V2 thinks you said:")
    user_msg_file = open("../micvadstreaming/results.txt", "r")
    user_msg = user_msg_file.read()
    user_msg_file.close()
    stt_end = time.time()
    print(user_msg)
        
    nlp_start = time.time()
    # NLP Portion of pipeline
    response = requests.post('http://localhost:5005/webhooks/rest/webhook',json={"sender": "test", "message": user_msg})

    # TTS Portion of pipeline
    tts_start = time.time()
    response_file = open("../rasa/response.txt", "w+")
    response_txt = ""
    for i in response.json():
        print(i['text'])
        response_file.write(i['text'])
        response_txt = response_txt + i['text']
    print("\n")

    audio = subprocess.Popen(['espeak -ven+f3 -k5 -s150', response_txt, '--stdout'], stdout=subprocess.PIPE)
    tts_end = time.time()
    aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
    audio.wait()
    aplay.wait()

    return user_msg

if __name__ == "__main__":
    # SIGINT Handler setup
    signal.signal(signal.SIGINT, signal_handler)

    # Start Rasa actions container
    subprocess.call("docker-compose run -d --rm --name rasa_actions rasa run actions > /dev/null 2>&1", shell=True)

    # Start Rasa server container
    subprocess.call("docker-compose run -d -p 5005:5005--rm --name rasa_server rasa run -m models --endpoints endpoints.yml > /dev/null 2>&1", shell=True)

    # Start DeepSpeech container
    subprocess.call("docker run -t -d --rm -w /dspeech --name micvad --device /dev/snd:/dev/snd cwrogers1/mamasara-deepspeech:micvad > /dev/null 2>&1", shell=True)
    subprocess.call("docker cp ../micvadstreaming/mvs_single.py micvad:./dspeech/mvs_single.py", shell=True)
    message = ''
    # Mama Sara Introduction
    intro = "Hello. How can I help?"
    audio = subprocess.Popen(['espeak', intro, '--stdout'], stdout=subprocess.PIPE)
    aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
    audio.wait()
    aplay.wait()

    while message.strip != "bye":
        message = conversation_event()

    print("Cleaning up...")
    subprocess.call("docker stop rasa_actions rasa_server micvad > /dev/null 2>&1", shell=True)
    subprocess.call("docker rm  rasa_actions rasa_server > /dev/null 2>&1", shell=True)
    print("Bye")
