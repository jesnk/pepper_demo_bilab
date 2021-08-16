#! /usr/bin/env python
# _*_ encoding: UTF-8 _*_

from naoqi import ALProxy
import sys, os
import time
import vision_definitions
from PIL import Image
import numpy as np
import pandas as pd
from datetime import datetime

ADDRESS = "192.168.1.188"
PORT = 9559

# naoqi Proxy 정의
motion = ALProxy("ALMotion", ADDRESS, PORT)
tts = ALProxy("ALTextToSpeech", ADDRESS, PORT)
video_device = ALProxy("ALVideoDevice", ADDRESS, PORT)

# 촬영 이미지 조건 설정
resolution = 2     #VGA
colorSpace = 11    #RGB
fps = 5
# set the condition
videoClient = video_device.subscribe("python_client", resolution, colorSpace, fps)

# 위치 및 모션 초기 조건 설정
useSensorValues = False
motion.moveInit()

# 기타 초기 설정
img_idx = 0
now = datetime.now()
date_time = now.strftime("%m-%d-%H:%M:%S")
img_dir = date_time
os.mkdir(img_dir)
img_location = pd.DataFrame({"img_num": [img_idx], "x_loc": [0], "y_loc": [0], "theta_loc": [0]})


while True:
    direction = raw_input("Where do you want to move? ")
    # 방향 이동 (i: 앞으로, k: 뒤로, j: 왼쪽으로, l: 오른쪽으로, p: 사진촬영, q: 나가기)
    # x(+: 앞 / -: 뒤 / 단위 0.1: 10cm), y(+: 왼 / -: 오 / 단위 0.1: 10cm), theta(+: 시계반대 / -: 시계 /단위: 1.57: 90도)
    if direction == 'i':
        id = motion.post.moveTo(0.5, 0, 0)
        tts.say("I'm moving forward")
        location = motion.getRobotPosition(useSensorValues)
        print("Position after Move: ", location)
        motion.wait(id, 0)
    if direction == 'k':
        id = motion.post.moveTo(-0.5, 0, 3.14)
        tts.say("I'm moving backward")
        location = motion.getRobotPosition(useSensorValues)
        print("Position after Move: ", location)
        motion.wait(id, 0)
    if direction == 'j':
        id = motion.post.moveTo(0, 0.5, 1.57)
        tts.say("I'm moving left")
        location = motion.getRobotPosition(useSensorValues)
        print("Position after Move: ", location)
        motion.wait(id, 0)
    if direction == 'l':
        id = motion.post.moveTo(0, -0.5, -1.57)
        tts.say("I'm moving right")
        location = motion.getRobotPosition(useSensorValues)
        print("Position after Move: ", location)
        motion.wait(id, 0)
    
    #사진 촬영
    if direction == 'p':
        # 사진 촬영
        img_idx += 1
        videoClient = video_device.subscribe("python_client", resolution, colorSpace, fps)
        naoImage = video_device.getImageRemote(videoClient)
        video_device.unsubscribe(videoClient)
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]
        image_string = str(bytearray(array))
        im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

        # 사진 파일 저장
        im.save("./" + img_dir + "/" + str(img_idx) + ".png", "PNG")
        im.show()

        # 사진 촬영 위치
        location = motion.getRobotPosition(useSensorValues)
        print("Position after taking Photo: ", location)
        img_location.loc[img_location.shape[0]] = [img_idx, location[0], location[1], location[2]]

    if direction == 'q':
        # 종료 시, 촬영한 전체 사진별 위치 csv 파일로 저장 
        img_location_data = pd.DataFrame(img_location)
        img_location_data.to_csv("./" + img_dir + "/" + str(date_time) + ".csv")
        break
