#!/usr/bin/python
# coding=utf-8

import time
import speech_recognition as sr
from gtts import gTTS
import vlc

from speech.speech import *

# Sensors
from sensors.sensors import (flame_sensor,
                             vibration_sensor,
                             laser_sensor,
                             gas_sensor)

# Commands 

from commands.wiki_info import SearchInfo
from commands.youtube import YouTube
from commands.weather import Weather
from commands.pubmed_news import PubMed
from commands.quotes import MTW2Quotes

import random

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

from RPi import GPIO

# GPIO channels.
LED_CHANNEL = 5

# Initialization GPIO channels
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_CHANNEL, GPIO.OUT)


### COMMANDS CONSTANTS
WEATHER_CITY = "https://www.weather-forecast.com/locations/Kyiv/forecasts/latest"
# YouTube commands
YOUTUBE = YouTube()

# Commands for getting news from pubmed
# Links URL to topics of interest to me for news from the pubmed.
CONNECTOME1 = "https://pubmed.ncbi.nlm.nih.gov/?term=connectome&sort=pubdate&sort_order=&size=10"
CONNECTOME2 = "https://pubmed.ncbi.nlm.nih.gov/31895746-the-relationship-between-cortical-thickness-and-language-comprehension-varies-with-sex-in-healthy-young-adults-a-large-sample-analysis/?from_term=connectome&from_sort=pubdate&from_sort_order=&from_size=100&from_pos=1"

CRISP1 = "https://pubmed.ncbi.nlm.nih.gov/?term=crisp&sort=pubdate&sort_order=&size=10"
CRISP2 = "https://pubmed.ncbi.nlm.nih.gov/31949024-performance-of-cardiovascular-risk-prediction-equations-in-indigenous-australians/?from_term=crisp&from_sort=pubdate&from_sort_order=&from_size=100&from_pos=1"

BRAIN_NEWS = PubMed(topic_url=CONNECTOME1,
                         article_url=CONNECTOME2)

CRISP_NEWS = PubMed(topic_url=CRISP1,
                    article_url=CRISP2)



### COMPUTER VISION CONSTANTS
# weights for semantic segmentation model
RPI_UNET_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights/unet.pt"
# weights for classification model
CLASSIFICATION_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights//mobilenet_v2-b0353104.pth"
# weights for style transfer models
SIMPSON_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights/simpsons.pth"
ABSTRACT_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights/abstract.pth"
OIL_WEIGHTS = "/home/pi/Downloads/test/computer_vision/weights/ftvangog.pth"#oil
DEVICE = "cpu"

### SYSTEM CONSTANTS
FOTO_FILE_PATH =  "/home/pi/Pictures/"
DATABASE_PATH = "/home/pi/home_ai/sensors/home.db"

########################### YouTube commands ###############################
while True:
    text = get_audio()
    
    if "turn on youtube" in text:
        
        speak("Принято!")
        YOUTUBE.later_watch()
        time.sleep(1)
        text = ""
        
    elif "stop" in text:
        
        YOUTUBE.pause()
        time.sleep(1)
        text = ""
        
    elif "turn off youtube" in text:
        
        YOUTUBE.exit()
        time.sleep(1)
        text = ""
       

########################## WIki commands ###################################
        

    elif "find information about" in text:
        data = text.split()[3:]
        print(data)
        
        if len(data) > 0:
            
            si = SearchInfo(*data)
            info = si.get_info().strip()
            mentions = si.get_mentions().strip()

            print(info,"------------", mentions)
            
            try:
                speak(mentions)
               
            except:
               speak(mentions)
               
            else:    
               text = ""

            text = ""
####################### Остальные команды ##########################
    elif "time" in text:
          
            t = time.strftime("%d/%m/%Y:%H:%M:%S", time.localtime())
            speak("it's" + str(t)+ "o'clock")
            text = ""

    elif "weather" in text:
        weather = Weather(url=WEATHER_CITY)
        w = weather.get_weather()
        speak(w)
        time.sleep(0.5)
        text = ""



    elif "latest news about brain" in text:# about human project
            
            title, news = BRAIN_NEWS.get_data()
            print("Title:",title, "\n",news)
            speak(news)
            time.sleep(0.5)
            text = ""
            
    elif "latest news about crisp" in text:
          
            title, news = CRISP_NEWS.get_data()
            speak(news)
            time.sleep(0.5)
            text = ""


    elif "proverb" in text:
           
        QUOTES = MTW2Quotes()
        q = MTW2Quotes()
        quote = q.get_quote()
        speak(quote)
        time.sleep(0.5)
        text = ""
            

    elif "temperature" in text:
        temp = 26#TemperaturAuswertung()

        #print("Temp:", temp)
        sensor_db = SensorsDB(db_path = DATABASE_PATH,
                             table_name="temperature",
                             value=float(temp))
        sensor_db.create_commit()

        speak("my lord, the temperature in your chamber is "+ str(temp)+ "degrees Celsius.")
        time.sleep(0.5)
        text = ""

    elif "turn on the light" in text:
        speak("my lord light is on")
        GPIO.output(5, False)
        text = ""
        
    elif "turn the lights off" in text:
        speak("my lord the light is off")
        GPIO.output(5, True)
        text = ""
 
######################### Computer Vision Commands #########################
             
    elif "classification" in text:
        
        model = MobileNetV2()
        model.load_state_dict(torch.load(CLASSIFICATION_WEIGHTS,
                                         map_location=DEVICE))
        model = model.eval()
        img_path = get_photo(FOTO_FILE_PATH)
        data = get_predict(img_path, model, labels)
        speak(f"In order of relevance found : {data[0]}, {data[1]}, {data[2]}")

    elif "semantic segmentation" in text:

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

    elif "style transfer" in text:
        speak("Which painting style do you want, my lord?")

    elif "composition" in text:

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


    elif "simpsons" in text:

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


    elif "van gogh starry night" in text:#картина маслом

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


