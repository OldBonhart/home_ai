import time
import random
import speech_recognition as sr
from gtts import gTTS
import vlc



def play_sound(filename):
    """
    Play sound with vlc player.
    """
    instance = vlc.Instance("--aout=alsa")
    p = instance.media_player_new()
    m = instance.media_new(filename)
    p.set_media(m)
    p.play()
    p.pause()
    vlc.libvlc_audio_set_volume(p, 100)

def speak(text):

    """
    make a speech from text
    and save as mp3 file,
    after that play it.
    """

    tts = gTTS(text=text,lang="en",)
    filename = "voice5.mp3"
    tts.save(filename)
    play_sound(filename)

def get_audio():

    """
    Returns text from speech.
    get audio from microphone,
    recognize and save as text.
    """

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak :")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=4)
        said = ""
        
        try:
            said = r.recognize_google(audio,language="en_US")
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
            #continue
    
    return said.lower()
