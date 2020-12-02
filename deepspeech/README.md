## Instructions to Run Container


1. Pull docker image from dockerhub onto Raspberry Pi, docker image is linux/armv7 based:\
`docker pull cwrogers1/mamasara-deepspeech:tflite`

2. Prepare audio file. You can use the provided testaudio.wav, or create your own audio file named testaudio.wav\
You can use a custom .wav file, but **you MUST ensure it is 16000Hz and mono audio ONLY** otherwise you may get erratic results.\
Sample command to convert audio files:\
`ffmpeg -i test.m4a -ac 1 test.wav` converts to mono .wav\
`sox test.wav -r 16000 test.wav` converts to 16000Hz

3. Copy STTscript.sh and testaudio.wav to Raspberry Pi.\
Note that you may have to give proper permissions for STTscript to be executed.

4. Run script to complete STT, ensure testaudio.wav is located in the same directory as STTscript.sh\
`./STTscript.sh`

## To build docker image

Command to build docker image:\
`docker buildx build --platform linux/arm/v7 -t cwrogers1/mamasara-deepspeech:tflite --push .`
