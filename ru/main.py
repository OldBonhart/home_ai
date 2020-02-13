#!/usr/bin/python
# coding=utf-8

import time
import random
import speech_recognition as sr
from gtts import gTTS
import vlc

from speech.speech import *

# Sensors
from sensors.sensors import (flame_sensor,
                             vibration_sensor,
                             laser_sensor,
                             gas_sensor)

from RPi import GPIO

# Commands

from commands.wiki_info import SearchInfo
from commands.youtube import YouTube
from commands.weather import Weather
from commands.neuro_news import NeuroNews
from commands.quotes import M2TWQuotes
from commands.advices import get_advice


# Computer Vision

import torch
import torchvision

from computer_vision.segmentation import SemanticSegmentation, UNet
from computer_vision.classification import MobileNetV2, get_predict
from computer_vision.style_transfer import NeuralStyleTransfer, TransformerNetwork
from computer_vision.utils import (get_photo,
                                   view_result,
                                   get_end_phrase,
                                   labels)



# GPIO channels.
LED_CHANNEL = 5

# Initialization GPIO channels
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_CHANNEL, GPIO.OUT)


### COMMANDS CONSTANTS
WEATHER_CITY = "https://sinoptik.ua/погода-киев"
# YouTube commands
YOUTUBE = YouTube()


### COMPUTER VISION CONSTANTS
# weights for semantic segmentation model
RPI_UNET_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights/unet.pt"
# weights for classification model
CLASSIFICATION_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights//mobilenet_v2-b0353104.pth"
# weights for style transfer models
SIMPSON_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights/simpsons.pth"
ABSTRACT_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights/abstract.pth"
OIL_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights/ftvangog.pth"#oil

# device on which a torch.Tensor is or will be allocated.
DEVICE = "cpu"

### SYSTEM CONSTANTS
FOTO_FILE_PATH =  "/home/pi/Pictures/"
DATABASE_PATH = "/home/pi/home_ai/sensors/home.db"

########################### YouTube commands ###############################
while True:
    text = get_audio()
    
    if "включить youtube" in text:
        
        speak("Принято!")
        YOUTUBE.later_watch()
        time.sleep(1)
        text = ""
        
    elif "пауза" in text:
        
        YOUTUBE.pause()
        time.sleep(1)
        text = ""
        
    elif "выключить youtube" in text:
        
        YOUTUBE.exit()
        time.sleep(1)
        text = ""
       

########################## WIki commands ###################################
        
    elif "найди информацию" in text:
        print(text)
        data = text.split()[2:]
        
        if len(data) > 0:
            
            si = SearchInfo(*data)
            info = si.get_info().strip()
            mentions = si.get_mentions().strip()

            print(info,"------------", mentions)
            if info != 'В Википедии нет статьи с таким названием.':
                speak(info)

            else:
                
               speak(info)

            text = ""
####################### Остальные команды ##########################
    elif "температура" in text:
        temp = TemperaturAuswertung()

        print("Temp:", temp)
        sensor_db = SensorsDB(db_path = DATABASE_PATH,
                             table_name="temperature",
                             value=float(temp))
        sensor_db.create_commit()

        speak("мой лорд, тепература в вашей опочивальне:"+ str(int(temp))+ "градусов по цельсию.")
        time.sleep(0.5)
        text = ""

    elif "включить свет" in text:
        speak("мой лорд, свет включен")
        GPIO.output(5, False)
        text = ""
        
    elif "выключить свет" in text:
        speak("мой лорд, свет выключен")
        GPIO.output(5, True)
        text = ""
      
            
    elif "время" in text:
        t = time.strftime("%d/%m/%Y:%H:%M:%S", time.localtime())
        speak("Сейчас" + str(t))
        text = ""

    elif "погода" in text:
            
        weather = Weather(WEATHER_CITY)
        w, n = weather.get_weather()
        speak(w)
        text = ""
        time.sleep(2)

    elif "народный прогноз погоды" in text:
            
        weather = Weather(WEATHER_CITY)
        w, n = weather.get_weather()
        speak(n)
        time.sleep(0.5)
        text = ""

    elif "новости" in text:
            
        nn = NeuroNews()
        news = nn.random_fresh_news()

        if len(news) != 0:
            speak(news)
            time.sleep(0.5)
            text = ""

        else:
            nn = NeuroNews()
            news = nn.random_fresh_news()
            speak(news)
            time.sleep(0.5)
            text = ""

    elif "цитата" in text:
           
        q = M2TWQuotes()
        quote = q.get_quote()
        speak(quote)
        time.sleep(0.5)
        text = ""
            
    elif "совет" in text:
            
        advice = get_advice()
        speak(advice)
        time.sleep(0.5)
        text = "" 
######################### Computer Vision Commands #########################
             
    elif "начать классификацию" in text:
        
        model = MobileNetV2()
        model.load_state_dict(torch.load(CLASSIFICATION_WEIGHTS,
                                         map_location=DEVICE))
        model = model.eval()
        img_path = get_photo(FOTO_FILE_PATH)
        data = get_predict(img_path, model, labels)
        speak(f"В порядке релевантности обнаружено : {data[0]}, {data[1]}, {data[2]}")

    elif "начать семантическую сегментацию" in text:

        model = UNet(n_classes=1)
        model.load_state_dict(torch.load(RPI_UNET_WEIGHTS,
                                         map_location=DEVICE))
        img_path = get_photo(FOTO_FILE_PATH )
        ss = SemanticSegmentation(model=model,
                                  img_path= img_path,
                                  img_size=256,
                                  fp_out=FOTO_FILE_PATH)
        filename = ss.get_segmentation()
        view_result(FOTO_FILE_PATH, filename)

    elif "начать перенос стиля" in text:
        speak(f"Какой из стилей живописи вам угодно, милорд?")

    elif "абстракция" in text:

        model = TransformerNetwork().to(DEVICE)
        model.load_state_dict(torch.load(ABSTRACT_WEIGHTS,
                                         map_location=DEVICE))
        img_path = get_photo(FOTO_FILE_PATH)
        simp = NeuralStyleTransfer(model=model,
                                input_img=img_path, 
                                img_size=400,
                                fp_out=FOTO_FILE_PATH,
                                device=DEVICE)

        filename = simp.get_style()
        speak(get_end_phrase())
        view_result(FOTO_FILE_PATH, filename)


    elif "симпсоны" in text:

        model = TransformerNetwork().to(DEVICE)
        model.load_state_dict(torch.load(SIMPSON_WEIGHTS,
                                         map_location=DEVICE))
        img_path = get_photo(FOTO_FILE_PATH)
        simp = NeuralStyleTransfer(model=model,
                                input_img=img_path, 
                                img_size=400,
                                fp_out=FOTO_FILE_PATH,
                                device=DEVICE)

        filename = simp.get_style()
        speak(get_end_phrase())
        view_result(FOTO_FILE_PATH, filename)


    elif "ван гог звездная ночь" in text:#картина маслом

        model = TransformerNetwork().to(DEVICE)
        model.load_state_dict(torch.load(OIL_WEIGHTS,
                                         map_location=DEVICE))
        img_path = get_photo(FOTO_FILE_PATH)
        simp = NeuralStyleTransfer(model=model,
                                input_img=img_path, 
                                img_size=400,
                                fp_out=FOTO_FILE_PATH,
                                device=DEVICE)

        filename = simp.get_style()
        view_result(FOTO_FILE_PATH, filename)
        speak(get_end_phrase())
