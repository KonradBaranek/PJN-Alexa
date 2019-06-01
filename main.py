import speech_recognition as sr

import console_parser


# obtain audio from the microphone
r = sr.Recognizer()

console_parser.load_config()

require_name = False

while(True):
  if True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=3)
        print("Say something!")
        audio = r.listen(source)
        try:
            ins = r.recognize_google(audio)
            print(ins)
            console_parser.parse(ins,require_name)
        except sr.UnknownValueError:
            print("I could not understand audio properly")
        except sr.RequestError as e:
            print("I could not request results from Google Speech Recognition service; {0}".format(e))
  else:
    print(">> ",end="")
    console_parser.parse(input())

