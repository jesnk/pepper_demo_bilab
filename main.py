# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time




def main(app):
    session = app.session
    tts = session.service("ALTextToSpeech")
    # tts.setLanguage("Korean")
    tts.setLanguage("English")
    # tts.say("hello! how may I help you?")
    tabletService = session.service("ALTabletService")

    # tabletService.showWebview()

    signalID = 0

    def callback(x, y):
        print "coordinate are x: ", x, " y: ", y
        if x > 640:
            # disconnect the signal
            tabletService.onTouchDown.disconnect(signalID)
            app.stop()


    signalID = tabletService.onTouchDown.connect(callback)
    app.run()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.125",
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.1.125'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["TabletModule", "--qi-url=" + connection_url])
        app.start()
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(app)
    print("Finishied")