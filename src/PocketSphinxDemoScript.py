'''
Script to demonstrate Pocketsphinx speech recognition accuracy
'''
import requests
import subprocess
import time

if __name__ == "__main__":
    
    message = ''
    while (message.strip() != "goodbye"):
        # STT portion of pipeline
        subprocess.call(['arecord', '-f', 'S16_LE', '-d', '5', '-r', '16000', '-c1', '--device', 'plughw:Device,0', '../speechrecording/request.wav'])
        
        stt_start = time.time()
        print("\nMamaSara V1 thinks you said:")
        subprocess.call(['../pocketsphinx/STTscript.sh'], shell=True)
        user_msg_file = open("../pocketsphinx/results.txt", "r")
        user_msg = user_msg_file.read()
        user_msg_file.close()
        stt_end = time.time()
        print(user_msg)
        #print("PocketSphinx Inference took {:.2f} seconds".format(stt_end - stt_start))

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
