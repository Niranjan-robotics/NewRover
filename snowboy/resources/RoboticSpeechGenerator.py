from gtts import gTTS
import os
import subprocess

def play_mp3(path):
    subprocess.Popen(['mpg123', '-q', path]).wait()

mytext = 'he he he'
tts = gTTS(mytext)
tts.save(mytext +'.mp3')

play_mp3(mytext +'.mp3')
