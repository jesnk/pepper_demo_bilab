import argparse
import sys
import time
import qi
from naoqi import ALProxy

from main_engversion import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=PEPPER_IP,
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.1.188'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()

    try:
        session.connect("tcp://" + PEPPER_IP + ":" + str(args.port))
    # print("connection complete")  # for debugging
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
               + "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    # execution
    Main(session).play()

    '''
    # When program exit, set default display page
    web page
    try:
        srv['tablet'] = session.service("ALTabletService")
        srv['tablet'].showWebview('http://198.18.0.1/apps/bi-html/home.html')
    except:
        pass
    '''
