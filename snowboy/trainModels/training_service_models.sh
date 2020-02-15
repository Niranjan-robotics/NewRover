#!/bin/bash

#========== how to create samples like "Alexa.pdml" ? models using mic ==========

#usage
#bash training_service_model.sh
#$pi@raspberrypi:~/snowboy $ 
#>record voice in 3 files (ex: come / go / stop / chappie / etc)
#arecord --format=S16_LE --duration=2 --rate=16000 --file-type=wav 1.wav
#arecord --format=S16_LE --duration=2 --rate=16000 --file-type=wav 2.wav
#arecord --format=S16_LE --duration=2 --rate=16000 --file-type=wav 3.wav
#>to listen to sound recorded : use folloinwg command
#	aplay --format=S16_LE --rate=16000 1.wav
#Now convert sample to model 
# python training_service.py 1.wav 2.wav 3.wav saved_model.pmdl
# finally rename this model "saved_model.pmdl" to recorded name
# test this using `replcaesaved to you actual name
#sudo python demo.py saved_model.pmdl
#=========================================================
~/snowboy
arecord --format=S16_LE --duration=5 --rate=16000 --file-type=wav 1.wav
arecord --format=S16_LE --duration=5 --rate=16000 --file-type=wav 2.wav
arecord --format=S16_LE --duration=5 --rate=16000 --file-type=wav 3.wav

sudo python training-service.py 1.wav 2.wav 3.wav saved_model.pmdl
