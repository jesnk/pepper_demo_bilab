# -*- encoding: UTF-8 -*-

import argparse
import sys
import time
import qi
from naoqi import ALProxy

from transition import *

# /opt/aldebaran/www/apps/bi-html/html/
DEFAULT_HTML_PAGE = 'http://198.18.0.1/apps/bi-html/home.html'
# the initial value of signalID (global value)
signalID = 0
VALID = 0.5


# class of the monitor screen with input values
class Monitor_input:
    def __init__(self, srv, touch_list=[], word_list=[]):
        self.target_touch_list = touch_list
        self.target_word_list = word_list
        self.srv = srv
        self.tabletService = srv['tablet']
        self.signalID = srv['tablet'].onTouchDown.connect(self.touch_callback)
        self.touched_position = None
        self.exit_flag = False
        self.ret = {}
        self.memory = srv['memory']
        self.asr = srv['asr']
        # self.asr.setLanguage("Korean")
        self.asr.setLanguage("English")

        # for debugging
        self.debug_mode = False
        self.debug_touch_count = 0
        self.debug_touch_coordinate = []

        try:
            self.asr.unsubscribe("asr")
        except:
            pass
        self.asr.pause(True)

    def check_valid_touch(self):
        for i in self.target_touch_list:
            if TOUCH_LIST[i]['x'][0] < self.touch_x < TOUCH_LIST[i]['x'][1]:
                if TOUCH_LIST[i]['y'][0] < self.touch_y < TOUCH_LIST[i]['y'][1]:
                    self.ret['touch_position'] = i
                    return True
        return False

    # for debugging
    def touch_callback(self, x, y):
        print(self.debug_mode)
        if self.debug_mode:
            self.debug_touch_count += 1
            self.debug_touch_coordinate.append([x, y])
            print("x: ", x, " y: ", y)
            if self.debug_touch_count == 4:
                self.debug_mode = False
                self.debug_touch_count = 0
                print("test")
                xs = [x[0] for x in self.debug_touch_coordinate]
                xs.sort()
                ys = [x[1] for x in self.debug_touch_coordinate]
                ys.sort()
                print("X range: ", xs[0], "-", xs[-1])
                print("Y range: ", ys[0], "-", ys[-1])
                print("Touch_debug_mode Finished")
                self.debug_touch_coordinate = []
                return
            return

        self.touch_x = x
        self.touch_y = y
        if self.check_valid_touch():
            self.ret['type'] = 'touch'
            self.ret['x'] = x
            self.ret['y'] = y
            self.exit_flag = True

        # print("class_ x ", x, " y ", y)  # for debugging

    # for debugging
    def asr_callback(self, msg):
        # Threshold
        print(msg[0], ' is recognized. ', msg[1])
        if msg[1] > VALID:
            print(msg[0], msg[1], " is returned")
            self.ret['type'] = 'speech'
            self.ret['word'] = msg[0]
            self.exit_flag = True

    def wait_for_get_input(self):
        print("target_word_list :",self.target_word_list)
        # self.asr.setLanguage("English")
        self.asr.pause(True)
        self.asr.setVocabulary(self.target_word_list, False)
        self.asr.pause(False)
        print("Staring wait", self.target_word_list)  # for debugging
        self.srv['audio_device'].setOutputVolume(3)

        try:
            self.asr.unsubscribe('asr')
        except:
            pass
        self.asr.subscribe('asr')

        asr_mem_sub = self.memory.subscriber("WordRecognized")
        asr_mem_sub.signal.connect(self.asr_callback)

        while not self.exit_flag:
            time.sleep(0.01)

        self.asr.unsubscribe('asr')
        self.srv['audio_device'].setOutputVolume(DEFAULT_VOLUME)
        self.exit_flag = False

        return self.ret

    def set_target_touch_list(self, touch_list):
        self.target_touch_list = touch_list

    def set_target_word_list(self, word_list):
        self.target_word_list = word_list

    def __del__(self):
        self.tabletService.onTouchDown.disconnect(self.touch_callback)
        self.asr.unsubscribe("ASR")


# class of the main progress
class Main:
    def __init__(self, session):
        self.srv = self.create_srv(session)
        self.monitor_input = Monitor_input(self.srv)

    def create_srv(self, session):
        srv = dict()
        srv['tablet'] = session.service("ALTabletService")
        srv['memory'] = session.service("ALMemory")
        srv['motion'] = session.service("ALMotion")
        srv['asr'] = session.service("ALSpeechRecognition")
        srv['tts'] = session.service("ALTextToSpeech")
        srv['aas'] = session.service("ALAnimatedSpeech")
        srv['audio_device'] = session.service("ALAudioDevice")
        srv['video_device'] = session.service("ALVideoDevice")
        srv['photo_capture'] = session.service("ALPhotoCapture")

        # for face detection
        srv['face_detection'] = session.service("ALFaceDetection")

        # set the audio
        srv['tts'].setVolume(0.1)  # [CHECK] Does this command set volume for entire scenario?
        srv['tts'].setParameter("defaultVoiceSpeed", 85)
        srv['audio_player'] = session.service("ALAudioPlayer")

        # Present Initial Page
        srv['tablet'].enableWifi()
        srv['tablet'].setOnTouchWebviewScaleFactor(1)
        srv['tablet'].showWebview('http://198.18.0.1/apps/bi-html/home.html')

        return srv

    def play(self):
        monitor_input = self.monitor_input
        srv = self.srv

        init_scene = 'home'
        scene_name, valid_touch_list, valid_word_list = \
            SCENES[init_scene][0], SCENES[init_scene][1], SCENES[init_scene][2]
        print(scene_name, valid_touch_list, valid_word_list)  # for debugging
        monitor_input.set_target_touch_list(valid_touch_list)
        monitor_input.set_target_word_list(valid_word_list)

        while True:
            input_ret = monitor_input.wait_for_get_input()
            ret = Transition().switch(srv, scene_name, input_ret)
            if ret is None:
                continue
            # print(ret)  # for debugging
            scene_name, valid_touch_list, valid_word_list = ret[0], ret[1], ret[2]
            monitor_input.set_target_touch_list(valid_touch_list)
            monitor_input.set_target_word_list(valid_word_list)
            if scene_name == 'exit':
                break

        srv['tablet'].hideWebview()
        # print("Finished")  # for debugging
