#
# a quick test for speech to text
#

import speech_recognition as sr
import webbrowser as wb

def main():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print ('say something')
        audio = r.listen(source)
        print ('done')
    try:
        text = r.recognize_google(audio)
        print('Neo said:\n' + text)
        #if 'telugu' in text:
         #   url ='https://www.youtube.com/results?search_query='
        url ='https://www.youtube.com/results?search_query='   
        wb.get().open_new(url + text)
    except Exception as e:
        print (e)
    except r.UnKnownValueError:
        print ('error')
    except r.RequestError as e:
        print ('failed'.format(e))


if __name__ == "__main__":
    main()

