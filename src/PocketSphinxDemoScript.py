'''
Script to demonstrate Pocketsphinx speech recognition accuracy
'''
import requests
import subprocess
import subprocess
import signal
import sys
import time

def signal_handler(sig, frame):
    print("Cleaning up Docker containers...")
    subprocess.call("sudo docker stop rasa_actions rasa_server > /dev/null 2>&1", shell=True)
    subprocess.call("sudo docker rm rasa_actions rasa_server > /dev/null 2>&1", shell=True)
    print("Bye!")
    sys.exit(0)
    return

if __name__ == "__main__":

    # Start Rasa containers
    print("Starting Rasa containers...")
    subprocess.call("sudo docker-compose run -d --rm --name rasa_actions rasa run actions > /dev/null 2>&1", shell=True)
    subprocess.call("sudo docker-compose run -d -p 5005:5005 --rm --name rasa_server rasa run -m models --endpoints endpoints.yml > /dev/null 2>&1", shell=True)
    time.sleep(45)
    print("Start up complete.")

    # SIGINT Handler setup
    signal.signal(signal.SIGINT, signal_handler)

    message = ''
    while (message.strip() != "goodbye"):
        # STT portion of pipeline
        subprocess.call(['arecord', '-f', 'S16_LE', '-d', '5', '-r', '16000', '-c1', '--device', 'plughw:Device,0', '/home/pi/MamaSara/pocketsphinx/request.wav'])
        
        stt_start = time.time()
        print("\nMamaSara V1 thinks you said:")
        subprocess.call(['/home/pi/MamaSara/pocketsphinx/pocketsphinx_script.sh'], shell=True)
        user_msg_file = open("/home/pi/MamaSara/pocketsphinx/results.txt", "r")
        user_msg = user_msg_file.read()
        user_msg_file.close()
        stt_end = time.time()
        print(user_msg)
        print("PocketSphinx Inference took {:.2f} seconds".format(stt_end - stt_start))

        if (user_msg.strip() == "goodbye"):
            break
        
        nlp_start = time.time()
        # NLP Portion of pipeline
        response = requests.post('http://localhost:5005/webhooks/rest/webhook',json={"sender": "test", "message": user_msg})
        nlp_end = time.time()
        print("Rasa NLP took {:.2f} seconds".format(nlp_end - nlp_start))
        
        # TTS Portion of pipeline
        tts_start = time.time()
        response_file = open("/home/pi/MamaSara/rasa/response.txt", "w+")
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
        print("espeak TTS took {:.2f} seconds".format(tts_end - tts_start))
