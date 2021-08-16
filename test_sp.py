# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeechRecognition Module"""

import qi
import argparse
import sys
import time


def asr_callback(msg) :
    print("Test")
    print(msg)
    return 0


def main(session):
    """
    This example uses the ALSpeechRecognition module.
    """
    # Get the service ALSpeechRecognition.

    asr_service = session.service("ALSpeechRecognition")
    asr_service.pause(True)

    asr_service.setLanguage("English")

    # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
    vocabulary = ["yes", "no", "please","hi","hello"]
    asr_service.setVocabulary(vocabulary, False)
    asr_service.pause(False)

    # Start the speech recognition engine with user Test_ASR
    asr_service.subscribe("Test_ASR")
    asr_mem_sub = session.service("ALMemory").subscriber("WordRecognized")
    asr_mem_sub.signal.connect(asr_callback)
    print 'Speech recognition engine started'
    # while True:  # for debugging
    #     time.sleep(0.1)

    asr_service.unsubscribe("Test_ASR")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.188",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
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
