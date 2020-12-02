# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import math
import subprocess
import time
import vision_definitions
import touch

RIGHT_SIDE = {"x":[880,1800], "y":[0,800],'name':"RIGHT_SIDE"}
LEFT_SIDE = {"x":[0,880], "y":[0,800],'name':"LEFT_SIDE"}



signalID = 0
def touch_callback(x, y) :
    print(" coordinate x : ",x, " y : ",y)
    print(signalID)

class Monitor_input :
    def __init__(self, tabletService, touch_list = [], word_list = []) :
	self.target_touch_list = touch_list
        self.target_word_list = word_list
	self.signalID = tabletService.onTouchDown.connect(self.touch_callback)
	self.tabletService = tabletService 
	self.touched_position = None
	self.exit_flag = False
	self.ret = {}
        self.memory = session.service("ALMemory")
        self.asr = session.service("ALSpeechRecognition")
        self.asr.pause(True)
        self.asr.setLanguage("Korean")
        try :
            self.asr.unsubscribe("asr")
        except :
            pass
        self.asr.pause(True)
        #asr.setAudioExpression(False)
        #asr_mem_sub = memory.subscribeToEvent('WordRecognized',"test_asr",'asr_callback')

        


    def check_valid_touch(self) :
	for i in self.target_touch_list :
	    if self.touch_x > i['x'][0] and self.touch_x < i['x'][1] :
		if self.touch_y > i['y'][0] and self.touch_y < i['y'][1] :
		    self.ret['touch_position'] = i['name']
		    return True
	return False

    def touch_callback(self,x,y) :
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

def main_tablet(session) :
 
    tabletService = session.service("ALTabletService")
    tts_service = session.service("ALTextToSpeech")
    tts_service.setLanguage("English")
    tts_service.setParameter("defaultVoiceSpeed", 70)
    tts_service.setVolume(0.5)

    print("Test")
    tabletService.enableWifi()
    #tabletService.loadApplication('browser')
    tts_service.say("hi")

    tabletService.showWebview("http://198.18.0.1/index.html")
    time.sleep(100)

    #tabletService.showWebview("http://198.168.1.125/home/nao/html/index.html")
    #tabletService.showWebview("http://198.18.0.1/index.html")
    tabletService.hideWebview()
    tabletService.showWebview("http://198.18.0.1/apps/bi-html/index.html")
    monitor_input = Monitor_input(tabletService)
    monitor_input.set_target_touch_list([LEFT_SIDE,RIGHT_SIDE])
    monitor_input.set_target_word_list(["안녕","페퍼","잘가","다음","처음"])

    while (True) :
	ret = monitor_input.wait_for_get_input()
	if ret['type'] == 'touch' :
	    if ret['touch_position'] == 'RIGHT_SIDE' :
		tts_service.say("Right side")
                tabletService.showWebview("http://198.18.0.1/apps/bi-html/1.html")
	    elif ret['touch_position'] == "LEFT_SIDE" :
		tts_service.say("Left side")
                tabletService.showWebview("http://198.18.0.1/apps/bi-html/index.html")
        elif ret['type'] == 'speech' :
            if ret['word'] == '잘가' :
                break
            if ret['word'] == '다음' :
                tabletService.showWebview("http://198.18.0.1/apps/bi-html/1.html")
            if ret['word'] == '처음' :
                tabletService.showWebview("http://198.18.0.1/apps/bi-html/index.html")


    print("passed 2")
    #global signalID
    #signalID = tabletService.onTouchDown.connect(touch_callback)

    tabletService.hideWebview()
    print("Finished")


def main_init(session) :
    """
        This is just an example script that shows how images can be accessed
        through ALVideoDevice in Python.
        Nothing interesting is done with the images in this example.
        """
    # Get the service ALVideoDevice.

    video_service = session.service("ALVideoDevice")

    # Register a Generic Video Module
    resolution = vision_definitions.kQQVGA
    colorSpace = vision_definitions.kYUVColorSpace
    fps = 20

    nameId = video_service.subscribe("python_GVM", resolution, colorSpace, fps)

    print 'getting images in remote'
    for i in range(0, 20):
        print "getting image " + str(i)
        img = video_service.getImageRemote(nameId)
        cv2.imshow(img)
        time.sleep(0.05)
    video_service.unsubscribe(nameId)






def main(session):
    navigation_service = session.service("ALNavigation")
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    tts_service = session.service("ALTextToSpeech")
    photo_capture_service = session.service("ALPhotoCapture")

    # tts.setLanguage("Korean")
    tts_service.setLanguage("English")
    # Say Emile in english
    tts_service.say("hello")
    if photo_capture_service.takePicture("/home/nao/jesnk/export","test2") :
        #print(subprocess.call(["bash", "/home/nao/jesnk/scp.sh","wpwp1"]))
        print("Success")
    else :
        print("Fail")


def main_video(session) :
    video_service = session.service("ALVideoRecorder")

    video_service.setCameraID(1)
    video_service.setFrameRate(30)
    video_service.setResolution(2)
    video_service.startRecording("/home/nao/jesnk/export","test_v1")
    time.sleep(5)
    videoInfo = video_service.stopRecording()
    print("Video was saved on the robot : ", videoInfo[1])
    print("Total number of frames : ",videoInfo[0])

def main_speech(session):
    asr_service = session.service("ALSpeechRecognition")
    asr_service.setLanguage("English")

    vocabulary = ["yes","no","please"]
    asr_service.pause(True)
    asr_service.removeAllContext()
    asr_service.setVocabulary(vocabulary,False)
    asr_service.subscribe("Test_ASR")
    print("Speech recognition engine started")
    time.sleep(20)
    asr_service.unsubscribe("Test_ASR")



############## TEST CODE ################
def main2(session) :
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("Crouch",2.0)

def main3(session) :
    navigation_service = session.service("ALNavigation")
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit",0.5)
    if False : #navigation_service.navigateTo(1.0,0.0) :
        print("True")
    else :
        print("False")
    if motion_service.moveTo(-1.0, 0.0, 0.0): # math.pi) :#math.pi) :
        print("True")
    else :
        print("False")
    #motion_service.moveTo(0.0,0.0,0.0)
    #navigation_service.startFreeZoneUpdate()

    '''
    navigationProxy.moveAlong(["Composed", \
                               ["Holonomic", ["Line", [1.0, 0.0]], 0.0, 5.0], \
                               ["Holonomic", ["Line", [-1.0, 0.0]], 0.0, 10.0]])
    '''
##################################



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.125",
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.1.123'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main_tablet(session)
    print("Finishied")
