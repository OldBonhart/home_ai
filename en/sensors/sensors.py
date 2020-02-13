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

FLAME_TITLE = "Fire Sensor"
VIBRATION_TITLE = "Vibration Sensor"
LASER_TITLE = "Laser System"
GAS_TITLE =  "Gas Sensor MQ-2"

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

    speak("Fire detected")
    time.sleep(2)
    flame_email.send_email()
    print("A fire message has been sent.")
    flame_db.create_commit()
    print("Fire data is recorded in the database.")

def vibration_callback(channel):

    speak("Hacking detected")
    time.sleep(2)
    vibration_email.send_email()
    print("A message about a hacking attempt has been sent.")
    vibration_db.create_commit()
    print("Hacking data is written to the database.")

def laser_callback(channel):

    speak("border violation detected")
    time.sleep(2)
    laser_email.send_email()
    print("A border violation message has been sent.")
    laser_db.create_commit()
    print("Border violation data is recorded in the database.")

def gas_callback(channel):

    speak("Gas leak detected")
    time.sleep(2)
    gas_email.send_email()
    print("A gas leak message has been sent.")
    gas_db.create_commit()
    print("Gas leakage data is recorded in the database.")

flame_sensor = GPIO.add_event_detect(FLAME_CHANNEL, GPIO.BOTH, bouncetime=300)
flame_sensor = GPIO.add_event_callback(FLAME_CHANNEL, flame_callback)

vibration_sensor = GPIO.add_event_detect(VIBRATION_CHANNEL, GPIO.BOTH, bouncetime=300)
vibration_sensor = GPIO.add_event_callback(VIBRATION_CHANNEL, vibration_callback)

laser_sensor = GPIO.add_event_detect(LASER_CHANNEL, GPIO.BOTH, bouncetime=300)
laser_sensor = GPIO.add_event_callback(LASER_CHANNEL, laser_callback)

gas_sensor = GPIO.add_event_detect(GAS_CHANNEL, GPIO.BOTH, bouncetime=300)
gas_sensor = GPIO.add_event_callback(GAS_CHANNEL, gas_callback)
