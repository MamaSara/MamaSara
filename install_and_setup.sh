
printf "#####Update and upgrade Raspberry Pi#####\n\n"
sudo apt-get update
sudo apt-get upgrade -y 
sudo apt-get dist-upgrade -y

printf "#####Install all dependencies for project with sudo######\n\n"
sudo apt-get install -y libbz2-dev libssl-dev build-essential tk-dev libncurses5-dev libncursesw5-dev\
 libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev\
 zlib1g-dev libffi-dev openjdk-8-jdk libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran python-dev\
 libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev\
 cython libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev python3-pip wget git 

printf "#####Install python3.7.8#####\n\n"
wget https://www.python.org/ftp/python/3.7.8/Python-3.7.8.tgz
sudo tar zxf Python-3.7.8.tgz
cd Python-3.7.8
sudo ./configure
sudo make -j 4
sudo make altinstall
printf "\n\n\n"

printf "#####Create and source a virtual environment, and upgrade pip and setuptools#####\n\n"
python3.7 -m venv ./MamaSaraV1_env
source ./MamaSaraV1_env/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
printf "\n\n\n"

printf "#####Install further dependancies with sudo#####\n\n"
sudo apt-get install libpcre3 libpcre3-dev alsa-utils mpg321 lame libasound-dev portaudio19-dev bison swig\
 libopenblas-dev libblas-dev m4 cmake cython python3-yaml python3-setuptools -y
printf "\n\n\n"

printf "#####Install additional dependancies with numpy#####\n\n"
sudo pip3 install scipy libatlas-base-dev tensorflow pandas pyttsx3 SpeechRecognition pyaudio numpy 
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
cd ../pocketsphinx-5prealpha
./configure
make
sudo make install
printf "\n\n\n"

printf "#####Clone git repository from Github#####\n\n"
git clone https://github.com/MamaSara/MamaSaraV1_PocketSphinx.git
printf "\n\n\n"

printf "\n\n\n########### Install of Rasa starts here ############\n\n"
printf" #####Install Poetry - a package management software used by Rasa#####\n\n"
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
source $HOME/.poetry/env
printf "\n\n\n"

printf "#####Install Bazel - to help with tensorflow dependancies#####\n\n"
git clone https://github.com/PINTO0309/Bazel_bin.git
cd Bazel_bin/2.0.0/Raspbian_Debian_Buster_armhf/openjdk-8-jdk
sudo chmod a+x install.sh
sudo ./install.sh
printf "\n\n\n"

printf "#####Install Tensorflow 2.1#####\n\n"
pip install keras_applications==1.0.8 --no-deps
pip install keras_preprocessing==1.1.0 --no-deps
pip install h5py==2.9.0 pybind11 six wheel mock
wget https://github.com/PINTO0309/Tensorflow-bin/raw/master/tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl
pip uninstall tensorflow -y
pip install tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl
printf "\n\n\n"

printf "#####Install tensorflow-addons 0.8.3#####\n\n"
git clone https://github.com/tensorflow/addons.git
cd addons
git checkout r0.8
python ./configure.py
bazel build --enable_runfiles build_pip_pkg
bazel-bin/build_pip_pkg artifacts
pip install artifacts/tensorflow_addons-*.whl
printf "\n\n\n"

printf "########## Install Rasa! - Note: poetry requires tensorflow-addons 0.8.2, but we installed tensorflow-addons 0.8.3 ##########\n\n"
printf "########## For the moment, change 'poetry.lock' entry for tensorflow-addons to 0.8.3 ##########\n\n"
d ~
git clone https://github.com/RasaHQ/rasa.git
cd rasa
git checkout 1.8.x
cp ../poetry.lock .
cp ../pyproject.toml .
make install
printf "\n\n\n"

printf "#####Install spaCy#####\n\n"
git clone https://github.com/explosion/spaCy
export BLIS_ARCH=generic
cd spaCy
pip install -r requirements.txt --user
python setup.py build_ext --inplace
pip install .
printf "\n\n\n"

### Usage
printf "Currently there is a bug with Rasa on Raspberry Pi. Discussed here:\n\
(https://forum.rasa.com/t/rasa-init-no-prompt-returns-notfounderror/25542/11)\n\
which causes some python related commands to fail, e.g. 'rasa train'.\n\
Fortunately there is a current, more or less convenient, workaround. Before executing a rasa command,\n\
simply prepend: 'LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1'."

#### Example usage
printf "mkdir demo_bot && cd demo_bot"
printf "Rasa usage:\n\tLD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 rasa init"
printf "Rasa usage:\n\tLD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 rasa init"

# Script exit
printf ""
printf ""
printf "------------------------------------------------------------"
printf "Congratulations! The MamaSaraV1 environment is now installed and ready for use on your Raspberry Pi"
printf "To test it out using the voice assistant:\n\t1. rasa run actions\n\t\
2. rasa shell"
printf "To test it out using the voice assistant:\n\t1. rasa run actions\
\n\t2. rasa run -m models --endpoints endpoints.yml\n\t3. python3 run.py"
printf "Don't forget to make use of the above "
printf "Enjoy MamaSaraV1!"
