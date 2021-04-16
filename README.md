# Mama Sara

World Vision Canada has identified a gap in accessible scientific information regarding general nutrition and healthcare for children in rural Kenya between zero and five years old. Recent reports by UNICEF show that the mortality rate among children between infancy and the age of five is 74 thousand per year, with 46% occurring during the first week of life. These reports go on to state that the large majority of these deaths can be attributed to malnutrition and lack of access to medical advice. Given the high English-speaking fluency proficiency among Kenyans, and relatively lower literacy rate, the offline voice assistant coined Mama Sara was initially proposed in 2019, at which time the first phase of the project was picked up by the 2019-2020 capstone team. The goal of this second phase of the project is to design and implement a prototype for the offline voice assistant to be used for feasibility testing by World Vision.

After various stages of research and testing, the team picked the Raspberry Pi 4 Model B as the main computer to implement the project on. Peripherals such as speaker, microphone, buttons, status LED, LCD display, and a power bank have been added to the prototype to make the testing unit more usable and portable. The core software architecture of the project consists of Speech-To-Text (STT), Natural Language Processing (NLP), and Text-To-Speech (TTS) modules. Due to the low voice recognition accuracy of the 2019-2020 final project, the Speech- To-Text component has been replaced with Mozilla DeepSpeech, a reliable, offline STT module. The team continues to use Rasa, the NLP module used in the first iteration, however the implementation of the module has been modified slightly to allow for easier communication with the voice assistant. The Text-to-Speech module has been modified such that the new module can be implemented on the mobile ARM architecture of the Raspberry Pi. In addition to adding software support for the various peripherals, the team also used Docker, an OS-level virtualization software, to reduce the overhead of scalability for the project when it comes to setting up the project environment.

Overall, the team has successfully achieved the goals of the project. A functional, standalone, prototype has been developed with the improved software modules embedded on the Raspberry Pi. Additionally, the start-up of the program has been automated and the response time of the software has been enhanced. The prototype is fully offline and can be tested in the service environment. The unit cost of the prototype is $295.38.

The GitHub repository of the 2019-2020 capstone team can be found at: https://github.com/EricBrine/Mama-Sara

The video presentation & demo for the 2020-2021 capstone can be found at the following link: https://play.library.utoronto.ca/01fb9f64f47a167ae5328d1f2e141adb

## Steps for Setting up the Mama Sara Application on a Raspberry Pi
1. With the official Raspberry Pi Imager software (available for download at: https://www.raspberrypi.org/software/), load a 32 Gb (or higher) Micro SD card with the Raspbian OS.
2. Once the Raspbian OS is loaded onto the Micro SD card, insert it into the Raspberry Pi and allow it to run through the boot up sequence and go through all of the prompts.
3. Clone this repository into the home directory of the Raspberry Pi (/home/pi/), the installation scripts depend on this.
4. Run the following command: source /home/pi/MamaSara/setup/install_and_setup.sh
5. Copy the indicated lines from /home/pi/MamaSara/automation/.bashrc to /home/pi/.bashrc to setup MamaSara application starting up automatically.

*Notes:*
- Throughout the setup and installation process, the raspberry pi must have a stable internet connection.
- After this is complete, the Mama Sara application can be run without the need for internet.
- To enable non-root access to docker and running containers, perform the following steps:
    1. sudo usermod -aG docker [user_name] (ex: sudo usermod -aG pi)
    2. log out and log back into device
- Be sure to right click on the Raspbian GUI speaker icon and select the appropriate output mode in the "Audio Outputs" dropdown.
- In order to run the main application, src/MamaSara.py, you need to have all necessary peripherals connected as outlined in the project report and presentation. If not, you will likely obtain erratic behavior due to uninitialized (and unchanging) pin values.

## To Use the Mama Sara application:
2. python3 /home/pi/MamaSara/src/MamaSara.py

## To test out Rasa with its interactive Shell:
2. sudo docker-compose run rasa run actions 
3. sudo docker-compose run rasa shell
