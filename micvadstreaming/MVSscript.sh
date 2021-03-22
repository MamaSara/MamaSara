#! /bin/bash

docker stop micvad
docker rm micvad
docker run -t -d -w /dspeech --name micvad --device /dev/snd:/dev/snd cwrogers1/mamasara-deepspeech:micvad
docker cp ./mvs_single.py micvad:./dspeech/mvs_single.py

while true
do
  echo Please speak now!
  docker exec -it micvad bash -c "python3 mvs_single.py -v 1 -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer --rate 44100" > /dev/null 2>&1
  docker cp micvad:/dspeech/results.txt ./results.txt
  echo Processing complete...
  echo Produced "results.txt":
  cat ./results.txt
done

docker stop micvad
