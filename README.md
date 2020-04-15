# home_ai
Voice assistant for Raspberry Pi with computer vision


## Commads

+ find information about [?] - information is parsed on Wikipedia and then voiced
+ time - voiced current time
+ weather - information is parsed on  nd then voiced
+ latest news about brain,crisp - information is parsed on [pubmed](https://www.ncbi.nlm.nih.gov/pubmed/) and then voiced
+ proverb - information is parsed on [site]() and then voiced
+ classification - pretrained on imagenet MobileNetv2 
+ semantic segmentation - pretrained on 10-12 images with "raspberry pi 0"
+ composition, simpsons, vang gogh starry night - neural style transfer
+ turn on youtube / turn off youtube, stop  - imitating human actions, interactions with YouTube

## Sensors
+ [rele module](https://www.amazon.com/Tolako-Arduino-Indicator-Channel-Official/dp/B00VRUAHLE) commands - turn on the light / turn the lights off 
+ [temperature module](https://www.amazon.com/DS18B20-Temperature-Measurement-Arduino-Starter/dp/B0786CZCYJ/ref=sr_1_5?dchild=1&keywords=DS18B20+module&qid=1586942077&sr=8-5) commands  - temperature
+ [flame sensor](https://www.amazon.com/SunFounder-Sensor-Module-Arduino-Raspberry/dp/B013G73F3W)
+ [MQ-2 sensor](https://www.amazon.com/Wavesahre-MQ-2-Gas-Sensor-Detection/dp/B00NJOIB50/ref=sr_1_1?dchild=1&keywords=MQ-2+sensor&qid=1586942135&s=electronics&sr=1-1)
+ [vibration sensor](https://www.amazon.com/Ximimark-Motion-Sensor-Vibration-Arduino/dp/B07TWQGMBY/ref=sr_1_3?dchild=1&keywords=vibration+sensor&qid=1586942151&sr=8-3)
+ Laser system consisting of [photoresistor module](https://www.amazon.com/uxcell-Intensity-Detection-Photoresistor-Digital/dp/B07W78QYJZ/ref=sr_1_7?dchild=1&keywords=photoresistor+module&qid=1586942168&sr=8-7) & [laser module](https://www.amazon.com/KY-008-Copper-Sensor-Module-Arduino/dp/B01CG52K1S)


## Files
+ [sensors]() code for sensors
+ [computer vision]() code for cv
+ [commands]() code for processing commands
+ [speech]() speech processing code
+ main.py -  main file 
