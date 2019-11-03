#
# a quick test for speech to text
#
import speech_recognition as sr
import webbrowser

def main():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        
        while True:
            print ('say something')
            audio = r.listen(source)
            try:
                result = r.recognize_google(audio)
                print("You said " + result)
                words = result.lower()
                if words.find("facebook"):
                    webbrowser.open('https://www.facebook.com')
                if words.find("google"):
                    webbrowser.open('https://www.google.co.uk')
                if words.find("stop"):
                    break
            except LookupError:
                print("Please, speak more clearly")
#             try:
#         text = r.recognize_google(audio)
#         print('Neo said:\n' + text)
#         if 'right' in text:
#             print('right found')
#         if 'left' in text:
#             print('left found')
#         if 'forward' in text:
#             print('forward found')
#         if 'backward' in text:
#             print('backward found')
#         if 'stop' in text:
#             print('stop found')
#     except Exception as e:
#         print (e)
#     except r.UnKnownValueError:
#         print ('error')
#     except r.RequestError as e:
#         print ('failed'.format(e))


if __name__ == "__main__":
    main()

