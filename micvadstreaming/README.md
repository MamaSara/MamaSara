# micvadstreaming

The "mvs_single.py" micvadstreaming script (adapted from https://github.com/mozilla/DeepSpeech-examples/) allows for real-time voice decoding using Mozilla DeepSpeech.\
VAD stands for Voice Activity Decection.

## Instructions to Run Demo Script

1. Pull docker image from dockerhub onto Raspberry Pi, docker image is linux/armv7 based:\
`docker pull cwrogers1/mamasara-deepspeech:micvad`

2. Copy MVSscript.sh and mvs_single.py to Raspberry Pi.\
Note that you may have to give proper permissions for MVSscript to be executed.

3. Run script to complete STT, it will run in an infinite loop, to end you must manually interrupt\
`./MVSscript.sh`
    * You can also suppress the output with something similar to this:\
    `./MVSscript.sh > /dev/null 2>&1`\
    `cat ./results.txt`
    
## Instructions to Run Image in General

From the MVSscript.sh file, these commands should be run:\

**1. Setup (to be run before STT operation):**
- Start Docker container\
`docker run -t -d -w /dspeech --name micvadtest --device /dev/snd:/dev/snd cwrogers1/mamasara-deepspeech:micvad`
- Copy Mic VAD Streaming single capture script into container (this is done seperately to facilitate easily changing it outside the Docker image)\
`docker cp ./mvs_single.py micvadtest:./dspeech/mvs_single.py`

**2. To record a single segment of speech:**
- Run command (does not print to terminal)\
`docker exec -it micvadtest bash -c "python3 mvs_single.py -v 1 -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer" > /dev/null 2>&1`
- Copy results to local host\
`docker cp micvadtest:/dspeech/results.txt ./results.txt`

**3. Shutdown**
- Stop and remove running Docker image so that it can cleanly run again next time\
`docker stop micvadtest`\
`docker rm micvadtest`

## To Build Docker Image from the Dockerfile (on MacOS)

Command to Build docker image:\
Ensure to run `docker login` first.
`docker buildx build --platform linux/arm/v7 -t cwrogers1/mamasara-deepspeech:micvad --push .`\
