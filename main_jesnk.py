# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import math
import subprocess
import time
import vision_definitions
import touch
from naoqi import ALProxy
from threading import Thread

sys.path.insert(0, './motion')
import entertain


FRAME_WIDTH = 1280
FRAME_HEIGHT = 800
DEFAULT_VOLUME = 60

# jesnk touch
TOUCH_LIST = {}
TOUCH_LIST['RIGHT_SIDE'] = {"x":[FRAME_WIDTH/2,FRAME_WIDTH], "y":[0,FRAME_HEIGHT],'name':"RIGHT_SIDE"}
TOUCH_LIST['LEFT_SIDE'] = {"x":[0,FRAME_WIDTH], "y":[0,FRAME_HEIGHT],'name':"LEFT_SIDE"}

TOUCH_LIST['JESNK_SIDE'] = {"x":[0,200], "y":[0,200],'name':"JESNK_SIDE"}

TOUCH_LIST['BUTTON_LEFT'] = {"x":[75,600], "y":[233,593],'name':"BUTTON_LEFT"}
TOUCH_LIST['BUTTON_RIGHT'] = {"x":[669,1192], "y":[227,598],'name':"BUTTON_RIGHT"}
TOUCH_LIST['BUTTON_MIDDLE_DOWN'] = {"x":[485,800], "y":[632,705],'name':"BUTTON_MIDDLE_DOWN"}
TOUCH_LIST['BUTTON_RIGHT_DOWN'] = {"x":[930,1156], "y":[641,707],'name':"BUTTON_RIGHT_DOWN"}
TOUCH_LIST['BUTTON_LEFT_DOWN'] = {"x":[150,390], "y":[621,707],'name':"BUTTON_LEFT_DOWN"}



scene_data = {}
scene_data['init'] = ['init',['RIGHT_SIDE','LEFT_SIDE'],['잘가','다음','처음']]
scene_data['1'] = ['1',['RIGHT_SIDE','LEFT_SIDE'],['잘가','다음','처음']]
scene_data['exit'] = ['exit',[],[]]

scene_data['home'] = ['home',['BUTTON_MIDDLE_DOWN','JESNK_SIDE'],['start','hi','pepper']]

scene_data['first_menu'] = ['first_menu',\
     ['JESNK_SIDE','BUTTON_RIGHT','BUTTON_LEFT',\
      'BUTTON_MIDDLE_DOWN','BUTTON_RIGHT_DOWN'],['잘가','다음','처음']]

scene_data['tour'] = ['tour',\
     ['JESNK_SIDE','BUTTON_RIGHT','BUTTON_LEFT',\
      'BUTTON_LEFT_DOWN','BUTTON_MIDDLE_DOWN','BUTTON_RIGHT_DOWN'],\
     ['잘가','다음','처음']]

scene_data['entertain'] = ['entertain',\
     ['JESNK_SIDE','BUTTON_RIGHT','BUTTON_LEFT',\
      'BUTTON_LEFT_DOWN','BUTTON_MIDDLE_DOWN','BUTTON_RIGHT_DOWN'],\
     ['잘가','다음','처음']]



signalID = 0
def touch_callback(x, y) :
    print(" coordinate x : ",x, " y : ",y)
    print(signalID)

class Monitor_input :
    def __init__(self, srv, touch_list = [], word_list = []) :
	self.target_touch_list = touch_list
        self.target_word_list = word_list
	self.tabletService = srv['tablet']
	self.signalID = srv['tablet'].onTouchDown.connect(self.touch_callback)
	self.touched_position = None
	self.exit_flag = False
	self.ret = {}
        self.memory = srv['memory']
        self.asr = srv['asr']
        self.asr.pause(True)
        self.asr.setLanguage("English")
        #self.asr.setLanguage("English")

        self.debug_mode = False
        self.debug_touch_count = 0
        self.debug_touch_coordinate = []
        try :
            self.asr.unsubscribe("asr")
        except :
            pass
        self.asr.pause(True)


    def check_valid_touch(self) :
	for i in self.target_touch_list :
	    if self.touch_x > TOUCH_LIST[i]['x'][0] and self.touch_x < TOUCH_LIST[i]['x'][1] :
		if self.touch_y > TOUCH_LIST[i]['y'][0] and self.touch_y < TOUCH_LIST[i]['y'][1] :
		    self.ret['touch_position'] = i
		    return True
	return False

    def touch_callback(self,x,y) :
        print(self.debug_mode)
        if self.debug_mode :
            self.debug_touch_count += 1 
            self.debug_touch_coordinate.append([x,y])
            print("x : ",x, " y : ",y)
            if self.debug_touch_count == 4 :
                self.debug_mode = False
                self.debug_touch_count = 0
                print("test")
                xs = [x[0] for x in self.debug_touch_coordinate]
                xs.sort()
                ys = [x[1] for x in self.debug_touch_coordinate]
                ys.sort()
                print("X range : ",xs[0],"-",xs[-1])
                print("Y range : ",ys[0],"-",ys[-1])
                print("Touch_debug_mode Finished")
                self.debug_touch_coordinate = []
                return
            return

	self.touch_x = x
	self.touch_y = y
	if (self.check_valid_touch()) :
	    self.ret['type'] = 'touch'
	    self.ret['x'] = x
	    self.ret['y'] = y
	    self.exit_flag = True

	print("class_ x ",x," y ",y)

    def asr_callback(self,msg) :
        # Threshold
        print(msg[0]," is recognized. ",msg[1])
        if msg[1] > 0.5 :
            print(msg[0],msg[1], " is returned")
            self.ret['type'] = 'speech'
            self.ret['word'] = msg[0]
            self.exit_flag = True

    def wait_for_get_input(self) :
        self.asr.setVocabulary(self.target_word_list,False)
        self.asr.subscribe('asr')
        asr_mem_sub = self.memory.subscriber("WordRecognized")
        asr_mem_sub.signal.connect(self.asr_callback)
        while not self.exit_flag :
	    time.sleep(0.01)

        self.asr.unsubscribe('asr')
	self.exit_flag = False
	return self.ret

    def set_target_touch_list(self,touch_list) :
	self.target_touch_list = touch_list
    def set_target_word_list(self, word_list) :
	self.target_word_list = word_list
    def __del__(self) :
	self.tabletService.onTouchDown.disconnect(self.touch_callback)
	self.asr.unsubscribe("ASR")





def get_html_address(file_name) :
    name = file_name
    if len(name) > 5 and name[-5:] == '.html' :
        name = name[:-5]
    return "http://198.18.0.1/apps/bi-html/" + name + '.html'


def transition(srv,scene,input_ret) :
    global monitor_input
    # return value : scene name, available touch, avail word
    print("Trainsition mode")
    print(scene,input_ret)

    if scene == 'home' :
        if input_ret['type'] == 'touch' :
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN' :
                next_scene = 'first_menu'

                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("다음")

                return scene_data[next_scene]


            # jesnk : test

            if input_ret['touch_position'] == 'JESNK_SIDE' :


                file_path = "/opt/aldebaran/www/apps/bi-sound/background.mp3"
                #srv['tts'].post.say('yes')
                player = ALProxy("ALAudioPlayer")
                player.post.playFileFromPosition(file_path,120)

                #file_id = srv['audio_player'].loadFile("/opt/aldebaran/www/apps/bi-sound/background.mp3")
                #srv['audio_player'].playFileFromPosition(file_path,120)

                #srv['audio_player'].setVolume(file_id,0.3)


        elif input_ret['type'] == 'speech' :
            if input_ret['word'] == 'start'  :
                next_scene = 'first_menu'
                srv['tablet'].showWebview(get_html_address(next_scene))

                return scene_data[next_scene]
        

    if scene == 'first_menu' :
        if input_ret['type'] == 'touch' :
            if input_ret['touch_position'] == 'JESNK_SIDE' :
                next_scene = 'first_menu'

                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("디버그")
                monitor_input.debug_mode = True

                while monitor_input.debug_mode :
                    time.sleep(0.01)
                srv['tts'].say("디버그 끝")

                return scene_data[next_scene]

            if input_ret['touch_position'] == 'BUTTON_LEFT' :
                next_scene = 'tour'

                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("다음")

                return scene_data[next_scene]

            if input_ret['touch_position'] == 'BUTTON_RIGHT' :
                next_scene = 'entertain'
                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("다음")
                return scene_data[next_scene]

            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN' :
                next_scene = 'home'
                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("다음")
                return scene_data[next_scene]
            if input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN' :
                next_scene = scene
                srv['tts'].say("내가 누구게???")
                return scene_data[next_scene]


    if scene == 'tour' :
        if input_ret['type'] == 'touch' :
            if input_ret['touch_position'] == 'BUTTON_LEFT' :
                next_scene = 'home'
                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("다음")
                return scene_data[next_scene]
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN' :
                next_scene = 'home'
                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("처음으로")
                return scene_data[next_scene]
            if input_ret['touch_position'] == 'BUTTON_LEFT_DOWN' :
                next_scene = 'first_menu'
                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("이전")
                return scene_data[next_scene]


    if scene == 'entertain' :
        if input_ret['type'] == 'touch' :
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN' :
                next_scene = 'home'
                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("처음으로")
                return scene_data[next_scene]
            if input_ret['touch_position'] == 'BUTTON_LEFT_DOWN' :
                next_scene = 'first_menu'
                srv['tablet'].showWebview(get_html_address(next_scene))
                srv['tts'].say("이전")
                return scene_data[next_scene]

            if input_ret['touch_position'] == 'BUTTON_LEFT' :
                # jesnk test
                #file_id = srv['audio_player'].loadFile("/opt/aldebaran/www/apps/bi-sound/test.mp3")
                #srv['audio_player'].setVolume(30)
                #srv['audio_player'].playFileFromPosition("/opt/aldebaran/www/apps/bi-sound/test.mp3",40)
                #srv['audio_player'].setVolume(DEFAULT_VOLUME)

                file_path = "/opt/aldebaran/www/apps/bi-sound/background.mp3"
                #srv['tts'].post.say('yes')
                player = ALProxy("ALAudioPlayer",PEPPER_IP,9559)
                player.post.playFileFromPosition(file_path,100)
                entertain.elephant(srv)
                player.post.stopAll()
                pass
            if input_ret['touch_position'] == 'BUTTON_RIGHT' :
                #Dance
                pass

# jesnk 1

    

monitor_input = None

def main(session) :
# jesnk main 
    print("Hello")
    srv = {}
    srv['tablet'] = session.service("ALTabletService")
    srv['memory'] = session.service("ALMemory")
    srv['motion'] = session.service("ALMotion")
    srv['asr'] = session.service("ALSpeechRecognition")
    srv['tts'] = session.service("ALTextToSpeech")
    srv['tts'].setVolume(0.1)
    srv['tts'].setParameter("defaultVoiceSpeed",70)
    srv['audio_player'] = session.service("ALAudioPlayer")

    # Present Inital Page
    srv['tablet'].enableWifi()
    srv['tablet'].setOnTouchWebviewScaleFactor(1)
    srv['tablet'].showWebview('http://198.18.0.1/apps/bi-html/home.html')
    # Valid Input condition setting
    global monitor_input
    monitor_input = Monitor_input(srv)

    init_scene = 'home'
    scene_name, valid_touch_list, valid_word_list = \
        scene_data[init_scene][0], scene_data[init_scene][1], scene_data[init_scene][2]
    print(scene_name, valid_touch_list, valid_word_list)
    monitor_input.set_target_touch_list(valid_touch_list)
    monitor_input.set_target_word_list(valid_word_list)

    while (True) :
        
	input_ret = monitor_input.wait_for_get_input()
        ret = transition(srv,scene_name,input_ret)
        if ret == None :
            continue
        print(ret)
        scene_name, valid_touch_list, valid_word_list = ret[0], ret[1], ret[2]
        monitor_input.set_target_touch_list(valid_touch_list)
        monitor_input.set_target_word_list(valid_word_list)
        if scene_name == 'exit' :
            break


    print("passed 2")
    #global signalID
    #signalID = tabletService.onTouchDown.connect(touch_callback)

    srv['tablet'].hideWebview()
    print("Finished")







PEPPER_IP = '192.168.1.123'
if __name__ == "__main__":

    print("Hello")
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default= PEPPER_IP,
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.1.123'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    print("Hello")

    args = parser.parse_args()
    session = qi.Session()
    print("Hello")
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    main(session)
