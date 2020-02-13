#sensors

from .database.sensors_database import SensorsDB
from .post.post_sender import SendEmail
from .post.post_content import html_content

from speech.speech import speak

from RPi import GPIO
import time

# logings and passwd for sending email
# and path to save database.
ADDR_FROM = ""
ADDR_TO = ""
PASSWD  = ""
DB_PATH = "home.database"

FLAME_TITLE = "Датчик пламени"
VIBRATION_TITLE = "Датчик вибрации"
LASER_TITLE = "Лазерная система"
GAS_TITLE =  "Датчик широкого спектра газов MQ-2"

# GPIO channels.
FLAME_CHANNEL =  13
VIBRATION_CHANNEL = 23
LASER_CHANNEL = 17
GAS_CHANNEL = 25


# Initialization GPIO channels
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_CHANNEL, GPIO.IN)
GPIO.setup(VIBRATION_CHANNEL, GPIO.IN)
GPIO.setup(LASER_CHANNEL, GPIO.IN)
GPIO.setup(GAS_CHANNEL, GPIO.IN)


# Sending email
flame_email = SendEmail(title=FLAME_TITLE,
                        content=html_content[FLAME_TITLE],
                        addr_from=ADDR_FROM,
                        addr_to=ADDR_TO,
                        passwd=PASSWD)

vibration_email = SendEmail(title=VIBRATION_TITLE,
                        content=html_content[VIBRATION_TITLE],
                        addr_from=ADDR_FROM,
                        addr_to=ADDR_TO,
                        passwd=PASSWD)

laser_email = SendEmail(title=LASER_TITLE,
                        content=html_content[LASER_TITLE],
                        addr_from=ADDR_FROM,
                        addr_to=ADDR_TO,
                        passwd=PASSWD)

gas_email = SendEmail(title=GAS_TITLE,
                        content=html_content[GAS_TITLE],
                        addr_from=ADDR_FROM,
                        addr_to=ADDR_TO,
                        passwd=PASSWD)

# Writing in database 
flame_db = SensorsDB(db_path=DB_PATH,
                     table_name="flame_sensor")

vibration_db = SensorsDB(db_path=DB_PATH,
                     table_name="vibration_sensor")
                     
laser_db = SensorsDB(db_path=DB_PATH,
                     table_name="laser_sensor")

gas_db = SensorsDB(db_path=DB_PATH,
                     table_name="gas_sensor")


def flame_callback(channel):

    speak("Обнаружено возгорание")
    time.sleep(2)
    flame_email.send_email()
    print("Сообщение об возгорании отправлено.")
    flame_db.create_commit()
    print("Данные о возгорании записаны в базу данных.")

def vibration_callback(channel):

    speak("Обнаружена попытка взлома")
    time.sleep(2)
    vibration_email.send_email()
    print("Сообщение о попытке взлома отправлено.")
    vibration_db.create_commit()
    print("Данные о попытке взлома записаны в базу данных.")

def laser_callback(channel):

    speak("Обнаружено нарушение границ.")
    time.sleep(2)
    laser_email.send_email()
    print("Сообщение об нарушении границ отправлено.")
    laser_db.create_commit()
    print("Данные о нарушении границы записаны в базу данных.")

def gas_callback(channel):

    speak("Обнаружена утечка газа")
    time.sleep(2)
    gas_email.send_email()
    print("Сообщение об утечке газа отправлено.")
    gas_db.create_commit()
    print("Данные об утечке газа записаны в базу данных.")

flame_sensor = GPIO.add_event_detect(FLAME_CHANNEL, GPIO.BOTH, bouncetime=300)
flame_sensor = GPIO.add_event_callback(FLAME_CHANNEL, flame_callback)

vibration_sensor = GPIO.add_event_detect(VIBRATION_CHANNEL, GPIO.BOTH, bouncetime=300)
vibration_sensor = GPIO.add_event_callback(VIBRATION_CHANNEL, vibration_callback)

laser_sensor = GPIO.add_event_detect(LASER_CHANNEL, GPIO.BOTH, bouncetime=300)
laser_sensor = GPIO.add_event_callback(LASER_CHANNEL, laser_callback)

gas_sensor = GPIO.add_event_detect(GAS_CHANNEL, GPIO.BOTH, bouncetime=300)
gas_sensor = GPIO.add_event_callback(GAS_CHANNEL, gas_callback)
