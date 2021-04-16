printf "Thank you for using this script"
printf "This script is stored at: https://github.com/MamaSara/MamaSara.git"
printf "This script assumes the MamaSara repository is stored in the Pi home directory, with path: ~/MamaSara/"
printf "This script will automatically be run in the setup directory of this repo, and will create the MamaSara_venv directory here"
printf "The installation is starting......\n\n\n"

printf "#####Update and upgrade Raspberry Pi#####\n\n"
sudo apt-get update
sudo apt-get upgrade -y 
sudo apt-get dist-upgrade -y
printf "\n\n\n"

printf "#####Install all dependencies for project with sudo######\n\n"
sudo apt-get install -y libbz2-dev libssl-dev build-essential tk-dev libncurses5-dev libncursesw5-dev\
 libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev\
 zlib1g-dev libffi-dev openjdk-8-jdk libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran python-dev\
 libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev\
 cython libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev python3-pip wget git curl python-rpi.gpio\
 python3-rpi.gpio espeak
print "\n\n\n"

printf "#####Install python3.7.8#####\n\n"
wget https://www.python.org/ftp/python/3.7.8/Python-3.7.8.tgz
sudo tar zxf Python-3.7.8.tgz
cd Python-3.7.8
sudo ./configure
sudo make -j 4
sudo make altinstall
cd ~
printf "\n\n\n"

printf "#####Upgrade pip and setuptools#####\n\n"
pip install --upgrade pip
pip install --upgrade setuptools
printf "\n\n\n"

printf "##### Put all executables in /home/pi/MamaSara/setup/bin #####"
cd /home/pi/MamaSara/setup/bin
printf "\n\n\n"

printf "#####Install Docker and Docker-Compose#####\n\n"
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose -y
printf "\n\n\n"

printf "#####Install further dependancies with sudo#####\n\n"
sudo apt-get install libpcre3 libpcre3-dev alsa-utils mpg321 lame libasound-dev portaudio19-dev bison swig\
 libopenblas-dev libblas-dev m4 cmake cython python3-yaml python3-setuptools -y
printf "\n\n\n"

printf "#####Install additional dependancies with pip#####\n\n"
sudo pip3 install scipy tensorflow pandas pyttsx3 SpeechRecognition pyaudio numpy pyyaml requests RPi.GPIO gpiozero board Adafruit-Blinka adafruit-circuitpython-charlcd
printf "\n\n\n"

printf "##### Pulling Rasa Docker Image from DockerHub #####"
sudo docker pull hoomant/mamasara:mamasara_rasa
printf "\n\n\n"

printf "##### Pulling DeepSpeech Docker Image from DockerHub #####"
sudo docker pull cwrogers1/mamasara-deepspeech:micvad
printf "\n\n\n"

cd ~
printf "\n\n------------------------------------------------------------"
printf "Congratulations! The MamaSara environment is now installed and ready for use on your Raspberry Pi"
printf "To test it out the MamaSara application:\n\t1. source ~/MamaSara_env/bin/activate\n\t2.python3 /home/pi/MamaSara/src/MamaSara.py"
printf "To test out Rasa with its interactive Shell:\n\t1. source ~/MamaSara_env/bin/activate\n\t2. sudo docker-compose run rasa run actions\n\t3. sudo docker-compose run rasa shell"
printf "IMPORTANT: To enable non-root access to docker and running containers, perform the following steps:\n\t1. sudo usermod -aG docker [user_name] (ex: sudo usermod -aG docker pi)\n\t2. Log out of user account and log back in for this to take effect.\n\nFor more information, refer to: https://phoenixnap.com/kb/docker-on-raspberry-pi"
printf "Enjoy MamaSara!"
