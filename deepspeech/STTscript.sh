#! /bin/bash

cd ~/dspeech
rm results.txt
docker rm dspeechtest
docker run -t -d -w /dspeech --name dspeechtest cwrogers1/mamasara-deepspeech:tflite
docker cp ../speechrecording/request.wav dspeechtest:/dspeech/request.wav
docker exec -it dspeechtest bash -c "deepspeech --model ./deepspeech-0.9.1-models.tflite --scorer ./deepspeech-0.9.1-models.scorer --audio ./request.wav > ./results.txt"
docker cp dspeechtest:/dspeech/results.txt ../deepspeech/results.txt
docker stop dspeechtest
echo
echo
echo
echo Processing complete...
echo Loaded "testaudio.wav" and produced "results.txt":
echo
cat ../deepspeech/results.txt
