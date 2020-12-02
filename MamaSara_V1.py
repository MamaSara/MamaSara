import requests
import subprocess

if __name__ == "__main__":
    
    message = ''
    while (message.strip() != "bye"):
        # STT portion of pipeline
        subprocess.call(['arecord', '-f', 'S16_LE', '-d', '5', '-r', '16000', '-c1', '--device', 'plughw:Device,0', 'testaudio.wav'])
        
        print("\nMamaSara V1 thinks you said:")
        subprocess.call(['pocketsphinx/STTscript.sh'], shell=True)
        user_msg_file = open("sphinx_results.txt", "r")
        user_msg = user_msg_file.read()
        user_msg_file.close()
        print(user_msg)
        print("\n")

        if (user_msg.strip() == "bye"):
            break

        # NLP Portion of pipeline
        response = requests.post('http://localhost:5005/webhooks/rest/webhook',json={"sender": "test", "message": user_msg})
        response_file = open("response.txt", "w+")
        response_txt = ""

        # TTS Portion of pipeline
        for i in response.json():
            print(i['text'])
            response_file.write(i['text'])
            response_txt = response_txt + i['text']
        print("\n")
        audio = subprocess.Popen(['espeak', response_txt, '--stdout'], stdout=subprocess.PIPE)
        aplay = subprocess.Popen(['aplay'], stdin=audio.stdout)
        audio.wait()
        aplay.wait()
