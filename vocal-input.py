#pip install SpeechRecognition 
#pip install PyAudio

import speech_recognition as sr
import os

# Record Audio
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)


# Speech recognition using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    #word = r.recognize_google(audio, language='en-EN')
    sentence = r.recognize_google(audio, language='it-IT')
    print("You said: " + sentence)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

#execute command
cmd = None
if("palla" in sentence): cmd = "followball"
if("gioc" in sentence): cmd = "followball"
if("faccia" in sentence): cmd = "followface"
if("sono" in sentence): cmd = "followface"
if("alza" in sentence): cmd = "standup"
if("relax" in sentence): cmd = "relax"
if("stop" in sentence): cmd = "relax"
if(cmd is not None):
    print("command: %s" % cmd)
    #os.system("python bb7.py " + cmd)
else:
    print("comando non riconosciuto")