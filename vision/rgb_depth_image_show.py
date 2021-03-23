
import qi
import argparse
import sys
from naoqi import ALProxy
from PIL import Image


def shot_rgb_t_camera(session):
    video_service = session.service("ALVideoDevice")
    fps = 20
    resolution = 2      # 0 == 160, 120 | 1 == 320, 240 | 2 == 640, 480
    colorSpace = 11     # 11 == bgr?
    name_id = video_service.subscribe("rgb_t", 0, resolution, colorSpace, fps)
    # video_service.subscribe(name, idx, resolution, color space, fps)

    for i in range(2):
        pepper_img = video_service.getImageRemote(name_id)
        width, height = pepper_img[0], pepper_img[1]
        array = pepper_img[6]
        img_str = str(bytearray(array))
        im = Image.frombytes("RGB", (width, height), img_str)
        im.save("image/rgb_"+str(i)+'.png', "PNG")

    video_service.unsubscribe(name_id)

def shot_depth_camera(session):
    video_service = session.service("ALVideoDevice")
    fps = 20
    resolution = 2
    colorSpace = 1  # 1 == obly Y(luma component) equivalent to one unsigned char
    name_id = video_service.subscribe("dep", resolution, colorSpace, fps)

    for i in range(2):
        pepper_img = video_service.getImageRemote(name_id)
        width, height = pepper_img[0], pepper_img[1]
        array = pepper_img[6]
        img_str = str(bytearray(array))
        im = Image.frombytes("L", (width, height), img_str)
        im.save("image/depth_"+str(i)+'.png', "PNG")

    video_service.unsubscribe(name_id)




### config ####
PEPPER_IP = '192.168.1.123'
parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, default=PEPPER_IP,
                    help="Robot IP address. On robot or Local Naoqi: use '192.168.1.123'.")
parser.add_argument("--port", type=int, default=9559,
                    help="Naoqi port number")
args = parser.parse_args()

##################################

if __name__ == "__main__":

    session = qi.Session()
    try:
        session.connect("tcp://" + PEPPER_IP + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
                          "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    # shot_camera(session)
    shot_depth_camera(session)


