import requests
import subprocess
import time
#import RPi.GPIO as GPIO
   
if __name__ == "__main__":
    #GPIO.setwarnings(False)
    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

    # Mama Sara Introduction
    intro = "Hello. How can I help?"
    audio = subprocess.Popen(['espeak', intro,'--stdout'], stdout=subprocess.PIPE)
    aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
    audio.wait()
    aplay.wait()

    # Start DeepSpeech container
    subprocess.call("docker run -t -d -w /dspeech --name micvad --device /dev/snd:/dev/snd cwrogers1/mamasara-deepspeech:micvad", shell=True)
    subprocess.call("docker cp ../micvadstreaming/mvs_single.py micvad:./dspeech/mvs_single.py", shell=True)
    message = ''
    while (message.strip() != "goodbye"):
        # Button integration, add event detection and wait for input
        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        subprocess.call("docker exec -it micvad bash -c \"python3 mvs_single.py -v 1 -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer --rate 44100\" > /dev/null 2&1", shell=True)
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

        #GPIO.cleanup()

    subprocess.call("docker stop micvad", shell=True)
    subprocess.call("docker rm micvad", shell=True)
