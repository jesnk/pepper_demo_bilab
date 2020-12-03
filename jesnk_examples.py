
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import math
import subprocess
import time
import vision_definitions
import touch







def init_say() :
    tts_service = session.service("ALTextToSpeech")
    tts_service.setLanguage("English")
    tts_service.setParameter("defaultVoiceSpeed", 70)
    tts_service.setVolume(0.5)
    #tabletService.loadApplication('browser')
    tts_service.say("hi")








class Scene :
    page = {}
    def __init__(self,file_name,service_dic) :
        self.file_name = file_name

    def set_available_touch(self,location_list) :
        self.available_touch_list = location_list


    def check_valid_touch(self, location) :
        for i in self.available_touch_list :
            if i == location :
                return True
        return False
class Scene_init(Scene) :

    def run_touch(self,location) :
        if not self.check_valid_touch(location) :
            return False
        if location == 'RIGHT_SIDE' :
            return [{'type':'transition','transition_to':'scene_1'}]


scene = {}




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





def main_prev(session):
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












