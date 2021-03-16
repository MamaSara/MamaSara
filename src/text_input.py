'''
Script that tests Rasa and TTS pipeline independant of STT
'''
import requests
import subprocess

if __name__ == "__main__":
    message = ''
    while (message.strip() != "bye"):
        # Get user request
        message = input("How can I help you?\n")
        # End transaction if user said "bye"
        if (message.strip() == "bye"):
            break
        # Rasa portion of pipeline
        response = requests.post('http://localhost:5005/webhooks/rest/webhook',json={"sender": "test", "message": message})
        response_file = open("response.txt", "w+")
        response_txt = ""
        for i in response.json():
            print(i['text'])
            response_file.write(i['text'])
            response_txt = response_txt + i['text']
        # TTS portion of pipeline
        audio = subprocess.Popen(['espeak', response_txt, '--stdout'], stdout=subprocess.PIPE)
        aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
        audio.wait()
