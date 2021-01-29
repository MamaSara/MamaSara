FROM debian:latest

RUN apt-get update

RUN apt-get install -y git python3-pip python3-scipy python3-numpy python3-pyaudio libatlas3-base curl
RUN pip3 install deepspeech --upgrade

RUN mkdir ./dspeech
WORKDIR "./dspeech"

RUN git clone https://github.com/mozilla/DeepSpeech-examples.git
RUN cp -a ./DeepSpeech-examples/mic_vad_streaming/. .

RUN pip3 install -r ./requirements.txt

RUN curl -LOk https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite
RUN curl -LOk https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
