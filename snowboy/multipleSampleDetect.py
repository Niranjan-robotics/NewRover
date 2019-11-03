#import snowboydecoder
import snowboydecoder 
import sys
import signal
import glob
import ntpath

interrupted = False

#this will get all models saved as pmdl's from a given folder.
all_paths=glob.glob("/home/pi/snowboy/trainModels/*.pmdl")

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

filePaths=[path_leaf(path) for path in all_paths]
print("Order of keywords")
callb=[]
i=0
for f in filePaths:
    i=i+1
    y=str(f).replace("pdml","")
    print(str(i) + "---->" + y)
    #--------- new addition ---------
    callb.append(lambda:snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING))




# Demo code for listening two hotwords at the same time
def hotWord(models):
    sensitivity = [0.5]*len(models)
    detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
    print('Listening... Press Ctrl+C to exit')
    callbacks=callb
    # main loop
    # make sure you have the same numbers of callbacks and models
    word = detector.start(detected_callback=callbacks, interrupt_check=interrupt_callback,sleep_time=0.03)

    return(word)

w = hotWord(all_paths)

print(w)
if w == '7':
    print("Yes")
elif word == '6':
    print("No")