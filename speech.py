# -*- encoding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import sys

sys.path.insert(0, './speech_recognition')
import audio

class saju(object):
    def __init__(self, srv):
        self.tts = srv['tts']
        self.asr = srv['asr']
        srv['asr'].setLanguage("English")
        self.exit_flag = False

    def asr_callback(self, msg):
        # Threshold
        if msg[1] > 0.4:
            print(msg[0], msg[1], " is returned")
            self.ret['type'] = 'speech'
            self.ret['word'] = msg[0]
            self.exit_flag = True

def main(srv):
    print("---Talk!---")
    #srv['tts'].say("Hello!")

    value = audio.get_string()

    print(value)
    return value
