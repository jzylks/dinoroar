import re
import os
import json

import RPi.GPIO as GPIO
import toml
from paho.mqtt.client import Client
import vlc
import random
import alsaaudio

DISABLE_MIC_AT_REST = False
STORY_PATH = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'stories')
PLAYER = vlc.MediaPlayer()
STORIES = [os.path.join(STORY_PATH, story) for story in os.listdir(STORY_PATH)]
with open('/etc/snips.toml') as f:
    CONFIG = toml.load(f)
with open('/usr/share/snips/assistant/assistant.json') as f:
    MODEL = json.load(f)
HOST = CONFIG['snips-common']['mqtt'].split(':')[0]
SITE = CONFIG['snips-audio-server']['bind'].split('@')[0]
CLIENT = Client()
CLIENT.username_pw_set(CONFIG['snips-common']['mqtt_username'], CONFIG['snips-common']['mqtt_password'])
if DISABLE_MIC_AT_REST:
    mix = alsaaudio.Mixer('Capture')


def disable_mic():
    if DISABLE_MIC_AT_REST:
        mix.setrec(0)


def enable_mic():
    if DISABLE_MIC_AT_REST:
        mix.setrec(1)


disable_mic()


def on_connect(client, userdata, flags, rc):
    client.subscribe("hermes/#")
    

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload
    if topic == "hermes/asr/startListening":
        listening_started()
    elif topic == "hermes/asr/stopListening":
        listening_stopped()
    elif re.match("hermes/hotword/.+/detected", topic):
        hotword_detected()
    elif re.match("hermes/intent/.+", topic):
        process_intent(json.loads(payload))
    elif topic.startswith("hermes/asr"):
        print(topic)
    else:
        print(topic)


def listening_started():
    enable_mic()
    print("Listening has started")


def listening_stopped():
    disable_mic()
    print("Listening has stopped")


def hotword_detected():
    print("Hotword detected")
    

def process_intent(message):
    print(message['intent']['intentName'])
    if message['intent']['intentName'] == 'jzylks:ReadStory':
        if PLAYER.is_playing():
            PLAYER.stop()
            print("Stopping playback")
        else:
            story = random.choice(STORIES)
            print("Starting playback: {}".format(story))
            PLAYER.set_mrl('file://' + story)
            PLAYER.play()

def button_pressed(event):
    print('Pressed')
    message = {'siteId': SITE, 'modelId': MODEL['id'], 'modelVersion': MODEL['version']['nluModel'], 'modelType': 'universal', 'currentSensitivity': 0.5}
    CLIENT.publish('hermes/hotword/default/detected', json.dumps(message))


def main():    
    CLIENT.on_connect = on_connect
    CLIENT.on_message = on_message
    CLIENT.connect(HOST)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(3, GPIO.FALLING)
    GPIO.add_event_callback(3, button_pressed)
    
    CLIENT.loop_forever()


if __name__ == '__main__':
    main()

