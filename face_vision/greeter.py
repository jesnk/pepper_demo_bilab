import qi
from naoqi import ALProxy
import time
import sys


class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, srv):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        # Connect the event callback.
        self.subscriber = srv['memory'].subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = srv['tts']
        self.fdt = srv['face_detection']
        self.fdt.subscribe("HumanGreeter")
        self.got_face = False  # initialisation

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        if not value:  # empty value when the face disappears
            self.got_face = False
        elif not self.got_face:  # only speak the first time a face appears
            self.got_face = True
            print "I saw a face!"
            self.tts.say("Hello, you!")
            # First Field = TimeStamp.
            timeStamp = value[0]
            print("TimeStamp is: " + str(timeStamp))  # for debugging
            # Second Field = array of face_Info's.
            faceInfoArray = value[1]
            for j in range(len(faceInfoArray) - 1):
                faceInfo = faceInfoArray[j]
                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]
                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]

                # for debugging
                print("Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2]))
                print("Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4]))
                print("Face Extra Infos :" + str(faceExtraInfo))

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print("Starting HumanGreeter")  # for debugging
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user, stopping HumanGreeter")
            self.fdt.unsubscribe("HumanGreeter")
            # stop
            sys.exit(0)
