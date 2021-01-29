import requests
import subprocess
import time
import RPi.GPIO as GPIO

#def button_callback_STT():
#    subprocess.call("docker", shell=True)
#    subprocess.call("docker", shell=True)

if __name__ == "__main__":
    
    # Mama Sara Introduction
    intro_file = open("../TTS/text_files/intro.txt", "w+")
    intro_file.write("Hello. How can I help?")
    intro = "ello. How can I help?"
    audio = subprocess.Popen(['espeak', intro,'--stdout'], stdout=subprocess.PIPE)
    aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
    audio.wait()
    aplay.wait()

    # Start DeepSpeech container
    subprocess.call("docker run -t -d -w /dspeech --name micvad --device /dev/snd:/dev/snd cwrogers1/mamasara-deepspeech:micvad", shell=True)
    subprocess.call("docker cp ../micvadstreaming/mvs_single.py micvad:./dspeech/mvs_single.py", shell=True)
    message = ''
    while (message.strip() != "goodbye"):
        # STT portion of pipeline
        subprocess.call("docker exec -it micvad bash -c \"python3 mvs_single.py -v 1 -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer --rate 44100\" > /dev/null 2>&1", shell=True)
        subprocess.call("docker cp micvad:/dspeech/results.txt ../micvadstreaming/results.txt", shell=True)
        print("\nMamaSara V2 thinks you said:")
        user_msg_file = open("../micvadstreaming/results.txt", "r")
        user_msg = user_msg_file.read()
        user_msg_file.close()
        stt_end = time.time()
        print(user_msg)

        if (user_msg.strip() == "goodbye"):
            break
        
        nlp_start = time.time()
        # NLP Portion of pipeline
        response = requests.post('http://localhost:5005/webhooks/rest/webhook',json={"sender": "test", "message": user_msg})
        nlp_end = time.time()
        #print("Rasa NLP took {:.2f} seconds".format(nlp_end - nlp_start))

        # TTS Portion of pipeline
        tts_start = time.time()
        response_file = open("../rasa/response.txt", "w+")
        response_txt = ""
        for i in response.json():
            print(i['text'])
            response_file.write(i['text'])
            response_txt = response_txt + i['text']
        print("\n")

        audio = subprocess.Popen(['espeak', response_txt, '--stdout'], stdout=subprocess.PIPE)
        tts_end = time.time()
        aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
        audio.wait()
        aplay.wait()
        #print("espeak TTS took {:.2f} seconds".format(tts_end - tts_start))
