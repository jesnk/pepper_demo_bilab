# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import math
import almath
import time

from naoqi import ALProxy

IP = "192.168.1.123"
PORT = 9559

try:
    faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
    print "Error when creating face detection proxy:"
    print str(e)
    exit(1)
period = 500
faceProxy.subscribe("Test_Face", period, 0.0)


class pepper(object):
    # Robot name
    robot_name = "pepper"

    def __init__(self):
        # 맞나...
        session.start()

        # Memory
        self.memory = self.session.service("ALMemory")

        # Posture
        self.posture = self.session.service("ALRobotPosture")
        self.tracker = self.session.service("ALTracker")
        self.tracker.registerTarget('Face', 0.1)

        # Text to speech
        self.tts = self.session.service("ALTextToSpeech")
        self.tts.setParameter("defaultVoiceSpeed", 100)
        self.tts.setVolume(0.5) # 0.5?1?

        # Speech Recognition
        self.asr = self.session.service('ALSpeechRecognition')
        self.asr.setLanguage("English")
        vocabulary = [self.robot_name, 'hi', 'yes', 'no']
        try:
            self.asr.unsubscribe("Test_ASR")
        except:
            print 'fail'
        self.asr.pause(True)
        self.asr.setVocabulary(vocabulary, False)
        self.asr.subscribe("Test_ASR")
        self.asr.setAudioExpression(False)
        self.asr_mem_sub = self.memory.subscriber("WordRecognized")
        self.asr_mem_sub.signal.connect(self.asr_callback)

        # Wave 수정중

        print 'ready'
        # self.say("ready")

    def asr_callback(self, msg):
        if msg[1] > 0.4:
            print msg
            if msg[0] == self.robot_name:
                robot_pepper.say(self.robot_name)
            elif msg[1] == 'hi':
                robot_pepper.say('hi')
            elif msg[2] == 'yes':
                robot_pepper.say('yes')


# def main(session):
#
#     robot_pepper = pepper(session)
#     robot_pepper.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.123",
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.1.123'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
        # app = qi.Application(["AL---", "--qi-url=" + "tcp://" + args.ip + ":" + str(args.port)])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
                                                                                              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    robot_pepper = pepper(session)
    robot_pepper.run()

    # main(session)
    print("Finishied")
