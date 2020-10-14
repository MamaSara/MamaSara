# install_rasa_on_pi.sh
# 
# use with raspian 2019-09-26-raspbian-buster.img
# tested with rasa 1.6.0
# 

# standard update
    
sudo apt update && sudo apt upgrade -y

# install latest pip

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py

# install dependencies

sudo apt install python3-dev libatlas-base-dev libhdf5-dev libblas-dev liblapack-dev gfortran -y

sudo pip install setuptools --upgrade --ignore-installed

sudo pip install wrapt --upgrade --ignore-installed

sudo pip install botocore

sudo pip install scipy==1.3.3

# download tensorflow 1.15
# thanks to PINTO0309!!
# https://github.com/PINTO0309

curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1GzjSi71jDUOVOoThEAtThEah5SqCoV59" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1GzjSi71jDUOVOoThEAtThEah5SqCoV59" -o tensorflow-1.15.0-cp37-cp37m-linux_armv7l.whl
echo Download finished.

sudo pip install tensorflow-1.15.0-cp37-cp37m-linux_armv7l.whl

sudo pip install rasa
echo ---------------------------------------------------------
echo "install complete!"
echo "*** NOTE ** rasa works fine with pre-trained models only!"
echo "training a model on the pi is not currently operational"
echo ---------------------------------------------------------