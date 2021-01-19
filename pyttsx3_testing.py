import pyttsx3;

engine = pyttsx3.init(driverName='nsss');

voices = engine.getProperty('voices');

for voice in voices:

        engine.setProperty('voice', voice.id);

        engine.say("I will speak this text");

        engine.runAndWait() ;
