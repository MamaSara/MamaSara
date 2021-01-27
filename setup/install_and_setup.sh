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
 cython libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev python3-pip wget git curl python3-rpi.gpio
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

printf "#####Create and source a virtual environment, and upgrade pip and setuptools#####\n\n"
python3.7 -m venv ./MamaSara_venv
source ./MamaSara_venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
cd MamaSara_venv
printf "\n\n\n"

printf "#####Install Docker and Docker-Compose#####\n\n"
curl https://raw.githubusercontent.com/oznu/docker-homebridge/master/raspbian-installer.sh?v=2019-12-11 -o get-homebridge.sh
chmod u+x get-homebridge.sh
./get-homebridge.sh
printf "Read the README file located at: https://github.com/oznu/docker-homebridge/wiki/Homebridge-on-Raspberry-Pi#quick-install/README for more information about this script"
printf "To manage Homebridge go to http://<ip of raspberry pi>:8080 in your browser. \n
 From here you can install, remove and update plugins, modify the Homebridge config.json\n
 and restart Homebridge. The default username is admin with password admin. Remember you \n
 will need to restart Homebridge to apply any changes you make to the config.json."
printf "\n\n\n"

printf "#####Install further dependancies with sudo#####\n\n"
sudo apt-get install libpcre3 libpcre3-dev alsa-utils mpg321 lame libasound-dev portaudio19-dev bison swig\
 libopenblas-dev libblas-dev m4 cmake cython python3-yaml python3-setuptools espeak -y
printf "\n\n\n"

printf "#####Install additional dependancies with pip#####\n\n"
sudo pip3 install scipy tensorflow pandas pyttsx3 SpeechRecognition pyaudio numpy pyyaml requests RPi.GPIO
printf "\n\n\n"

printf "#####Install pytorch#####\n\n"
git clone --recursive https://github.com/pytorch/pytorch
cd pytorch
export NO_CUDA=1
export NO_DISTRIBUTED=1
export NO_MKLDNN=1 
export NO_NNPACK=1 
export NO_QNNPACK=1
python3 setup.py build
cd ..
printf "\n\n\n"

printf "#####Install PocketSphinx#####\n\n"
wget https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz/download -O sphinxbase.tar.gz
wget https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz/download -O pocketsphinx.tar.gz
tar -xzvf sphinxbase.tar.gz
tar -xzvf pocketsphinx.tar.gz
cd sphinxbase-5prealpha
./configure --enable-fixed
make
sudo make install

cd ../pocketsphinx-5realpha
# Update continous.c file for pocketsphinx to suit our purposes
cp ~/MamaSara/pocketsphinx/continous.c src/programs/
# Continue with setup
./configure
make
sudo make install
cd ..
printf "\n\n\n"

printf "##### Install Rasa through docker #####"
git clone https://github.com/koenvervloesem/rasa-docker-arm.git
cd rasa-docker-arm
cp ~/MamaSara/rasa/rasa_docker/Makefile .
cp ~/MamaSara/rasa/rasa_docker/build_docker.sh scripts/
cp ~/MamaSara/rasa/rasa_docker/rasa-1.10.16-arm.patch patches/
cp ~/MamaSara/rasa/rasa_docker/docker-compose.yml .
make docker

cd ~
printf "\n\n------------------------------------------------------------"
printf "Congratulations! The MamaSaraV1 environment is now installed and ready for use on your Raspberry Pi"
printf "To test it out using the voice assistant:\n\t1. docker-compose run rasa run actions\n\t2. docker-compose run rasa shell"
printf "To test it out using the voice assistant:\n\t1. docker-compose run rasa run actions\n\t2. docker-compose run rasa run -m models --endpoints endpoints.yml\n\t3. python3 run.py"
printf "IMPORTANT: Remember to logout of raspberry pi to enable Docker with the correct permissions"
printf "Enjoy MamaSaraV1!"
