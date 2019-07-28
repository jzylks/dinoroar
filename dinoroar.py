import re
import os
import json
from subprocess import Popen

import RPi.GPIO as GPIO
import toml
from paho.mqtt.client import Client
import random


class Dinoroar:

    action_sub = None
    mqtt_client = None
    
    def __init__(self):
        story_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'stories')
        assets_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'assets')
        startup_sub = Popen(['mpg123', os.path.join(assets_path, 'lotus-by-kevin-macleod.mp3')])
        self.stories = [os.path.join(story_path, story) for story in os.listdir(story_path)]
        with open('/etc/snips.toml') as f:
            self.snips_config = toml.load(f)
        with open('/usr/share/snips/assistant/assistant.json') as f:
            self.snips_model = json.load(f)
        self.snips_site = self.snips_config['snips-audio-server']['bind'].split('@')[0]
        self._initialize_mqtt()
        self._initialize_gpio()
        startup_sub.terminate()

    def _initialize_mqtt(self):
        host = self.snips_config['snips-common']['mqtt'].split(':')[0]
        self.mqtt_client = Client()
        self.mqtt_client.username_pw_set(self.snips_config['snips-common']['mqtt_username'], self.snips_config['snips-common']['mqtt_password'])
        self.mqtt_client.on_connect = self.mqtt_on_connect
        self.mqtt_client.on_message = self.mqtt_on_message
        self.mqtt_client.connect(host)

    def _initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(3, GPIO.FALLING)
        GPIO.add_event_callback(3, self.button_pressed)

    def mqtt_on_connect(self, client, userdata, flags, rc):
        client.subscribe("hermes/#")

    def mqtt_on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload
        if topic == "hermes/asr/startListening":
            self.listening_started()
        elif topic == "hermes/asr/stopListening":
            self.listening_stopped()
        elif re.match("hermes/hotword/.+/detected", topic):
            self.hotword_detected()
        elif re.match("hermes/intent/.+", topic):
            self.process_intent(json.loads(payload))
        elif topic.startswith("hermes/asr"):
            print(topic)
        else:
            print(topic)

    def listening_started(self):
        print("Listening has started")

    def listening_stopped(self):
        print("Listening has stopped")

    def hotword_detected(self):
        print("Hotword detected")
        if self.action_sub:
            self.action_sub.terminate()
            self.action_sub = None

    def process_intent(self, message):
        print(message['intent']['intentName'])
        if message['intent']['intentName'] == 'jzylks:ReadStory':
            story = random.choice(self.stories)
            self.action_sub = Popen(['mpg123', story])

    def button_pressed(self, event):
        print('Pressed')
        message = {
            'siteId': self.snips_site, 
            'modelId': self.snips_model['id'],
            'modelVersion': self.snips_model['version']['nluModel'],
            'modelType': 'universal',
            'currentSensitivity': 0.5
        }
        self.client.publish('hermes/hotword/default/detected', json.dumps(message))

    def listen(self):
        self.mqtt_client.loop_forever()


def main():
    dinoroar = Dinoroar()
    dinoroar.listen()


if __name__ == '__main__':
    main()

