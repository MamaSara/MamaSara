FROM debian:latest

RUN apt-get update

RUN apt-get install -y git python3-pip python3-scipy python3-numpy python3-pyaudio libatlas3-base curl
RUN pip3 install deepspeech --upgrade

RUN mkdir ./dspeech

RUN cd ./dspeech && curl -LOk https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-models.tflite
RUN cd ./dspeech && curl -LOk https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-models.scorer
