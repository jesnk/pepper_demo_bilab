# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import math


def main(session):
    tts = session.service("ALTextToSpeech")

    # tts.setLanguage("Korean")
    tts.setLanguage("English")
    # Say Emile in english
    tts.say("hello")



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
    parser.add_argument("--ip", type=str, default="192.168.1.123",
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
    main(session)
    print("Finishied")