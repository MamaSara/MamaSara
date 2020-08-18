import pyttsx3 as tts
import argparse
import requests
import speech_recognition as sr


class MamaSara:

    def __init__(self):
        self.r = sr.Recognizer()
        self.tts_engine = tts.init()

    @staticmethod
    def text_bot():
        sender = input("What is your name?\n")

        message = ""
        while message != "stop":

            # Gets user input.
            message = input("What's your message?\n")

            print("Sending message now...")

            # Sends user input to Rasa server and receives response.
            r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": sender, "message": message})

            # Print out response to user.
            print("Bot says, ")
            for i in r.json():
                print(f"{i['text']}")

        print("Bye, ", sender)

    def speech_bot(self):

        mic = sr.Microphone()

        with mic as source:
            self.r.adjust_for_ambient_noise(source)

        audio_string = ''
        while audio_string.strip() != "bye":

            # Gets user audio input.
            with mic as source:
                self.r.adjust_for_ambient_noise(source)
                print("Say something!")
                audio = self.r.listen(source)

            # Attempts Speech-to-Text.
            try:
                message = self.r.recognize_sphinx(audio)
                print("Sphinx thinks you said " + message + "\n")
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))

            print("Sending message now...")

            # Sends user input to Rasa server and receives response.
            r = requests.post('http://localhost:5005/webhooks/rest/webhook',
                              json={"sender": "test", "message": message})

            # Output response.
            print("Bot says, ")
            for i in r.json():
                print(i['text'])
                self.tts_engine.say(i['text'])
                self.tts_engine.runAndWait()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Mama Sara")
    parser.add_argument(
        "-m",
        "--mode",
        default="speech",
        help="Path to the model directory which contains "
             "sub-folders for core and nlu models.",
    )
    args = parser.parse_args()
    print(args.mode)
    mama_sara = MamaSara()

    # Runs method for voice-controlled virtual assistant.
    if args.mode == "speech":
        mama_sara.speech_bot()

    # Runs method for text-based command line virtual assistant.
    elif args.mode == "text":
        mama_sara.text_bot()
    else:
        print("Invalid argument.")

