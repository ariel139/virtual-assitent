import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import sys
from docx import Document
import geocoder
import requests
import json
from json.decoder import JSONDecodeError

talking = True

r = sr.Recognizer()
desktop = os.path.expanduser("~/Desktop")
if '\\' in desktop:
    desktop = desktop.replace('\\','/')

mic = sr.Microphone(device_index=2)


def speck(text):
    spech = gTTS(text, lang = 'en')
    spech.save('spech.mp3')
    playsound('spech.mp3')
    os.remove('spech.mp3')

def recognize():
    with mic as sourse:
        audio = r.listen(sourse)
    text = r.recognize_google(audio)
    return text

def documents():
    print('How do want to call your file?')
    speck('How do want to call your file? (please say it).')

    name_of_file = recognize()
    print('start talking')
    speck('start talking, ')
    doc = Document()


    data = recognize()
    with open(f'{desktop}/{name_of_file}.txt', 'w') as myfile:
        myfile.write(data)
    with open(f'{desktop}/{name_of_file}.txt','r',encoding='utf-8') as file:
        doc.add_paragraph(file.read())
        doc.save(f'{desktop}/{name_of_file}.docx')
    os.remove(f'{desktop}/{name_of_file}.txt')

    print('The file saved on your desktop')
    speck('the file saved on your desktop. thank you!')

def wether():
    me = geocoder.ip('me')
    cords = me.latlng
    lat = cords[0]
    lang = cords[1]
    weather = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lang}&units=metric&appid=b7830cb6712606dd3a60ce03794cf408')
    weather_json = json.loads(weather.text)
    speck(f'the weather is {weather_json["main"]["temp"]} celsius degrees')

username = sys.argv[1]
