# Record with 44100 Hz sampling rate and put the resulting file in test.wav then play test.wav 

arecord -D plughw:Device, 0 –format S16_LE –rate 44100 -c1 -d 10 test.wav
aplay test.wav
