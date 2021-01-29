#! /bin/bash

docker stop micvadtest
docker rm micvadtest
docker run -t -d -w /dspeech --name micvadtest --device /dev/snd:/dev/snd cwrogers1/mamasara-deepspeech:micvad
docker cp ./mvs_single.py micvadtest:./dspeech/mvs_single.py

while true
do
  echo Please speak now!
  docker exec -it micvadtest bash -c "python3 mvs_single.py -v 1 -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer" > /dev/null 2>&1
  docker cp micvadtest:/dspeech/results.txt ./results.txt
  echo Processing complete...
  echo Produced "results.txt":
  cat ./results.txt
done

docker stop micvadtest
