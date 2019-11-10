#
# a quick test for speech to text
#
import speech_recognition as sr
import os,sys,signal

def main():

    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print ('say something')
        audio = r.listen(source)
        print ('done')
    try:
        text = r.recognize_google(audio)
        print('Neo said:\n' + text)
        if 'right' in text:
            print('right found')
        if 'left' in text:
            print('left found')
        if 'forward' in text:
            print('forward found')
        if 'backward' in text:
            print('backward found')
        if 'stop' in text:
            print('stop found')
    except Exception as e:
        print (e)
    except r.UnKnownValueError:
        print ('error')
    except r.RequestError as e:
        print ('failed'.format(e))


if __name__ == "__main__":
    #pid=os.getpid()
    main()
    sys.exit()
    #os.kill(pid,signal.SIGTERM)

