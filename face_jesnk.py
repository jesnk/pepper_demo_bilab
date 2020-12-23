# -*- encoding: UTF-8 -*-
import qi
import argparse
import sys
import math
import subprocess
import time
import vision_definitions
import touch
import numpy as np
import cv2
from naoqi import ALProxy
from threading import Thread
import face_recognition



SUB_NAME = 'fr2'


def face_test(srv) :
    srv['tablet'].showWebview('http://198.18.0.1/apps/bi-html/keyboard_test.html')
    srv['tts'].say("얼굴 인식 테스트 모듈을 시작합니다.")
    face_list = []
    jesnk_face = face_recognize(srv)
    jesnk = {}
    jesnk['face_encoding'] = jesnk_face
    jesnk['name'] = "강제순"
    face_list.append(jesnk)
    face_detection(srv,face_list)


def face_recognize(srv) :
    srv['tts'].say("얼굴 스캐닝 시작")
    #srv['tts'].say("I'll starting face scan after 2 seconds")
    time.sleep(2)

    face_dir_path = "/home/jesnk/pepper/img/face_test/"

    srv['video'].unsubscribe(SUB_NAME)
    rgb_top = None
    idx = 0
    while not rgb_top :
        rgb_top = srv['video'].subscribeCamera(SUB_NAME+str(idx),0,2,11,5) #name, idx, resolution,colorspace, fps
        idx +=1

    cams = []
    cams.append(rgb_top)

    file_no = 0

    find_face_flag = False

    while (not find_face_flag):
	for cam in cams :
	    msg = srv['video'].getImageRemote(cam)
	    if msg is None :
		print(cam, " not returned data")
		continue
	    w = msg[0]
	    h = msg[1]
	    c = msg[2]
	    data = msg[6]
	    ba = str(bytearray(data))

	    nparr = np.fromstring(ba, np.uint8)
	    img_np = nparr.reshape((h, w, c))
	    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

	    #self.pio.vision.video.setResolution(self.pio.vision.rgb_top, 2)
            #cv2.imshow('window',img_np)

	    #cv2.imwrite(face_dir_path+str(file_no) + ".jpg", img_np)
            #picture_of_me = face_recognition.load_image_file(face_dir_path+str(file_no)+ ".jpg")
            print(cam," ",file_no, " is saved")

            face = face_recognition.face_encodings(img_np)
            if face :
                print("face detected, {}".format(face))
                find_face_flag = True
            file_no +=1 
    srv['tts'].say("얼굴 인식 완료")

    return face[0]
    

    # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!
    #


def face_detection(srv,face_list) :

    srv['video'].unsubscribe(SUB_NAME)
    rgb_top = None
    idx = 0
    while not rgb_top :
        rgb_top = srv['video'].subscribeCamera(SUB_NAME+str(idx),0,2,11,5) #name, idx, resolution,colorspace, fps
        idx +=1
    cams = []
    cams.append(rgb_top)
    face_dir_path = "/home/jesnk/pepper/img/face_test/"


    srv['tts'].say("얼굴 인식을 시작합니다.")


    frame_no = 0
    while (True):
	for cam in cams :
            interval_count = 0
            start = time.time()
            # 0
	    msg = srv['video'].getImageRemote(cam)
            # 1
            ### TIME PROFILE
            interval = time.time() - start
            interval_count += 1
            #print("{} to {} : {}".format(interval_count-1, interval_count,interval))
            ### TIME PROFILE

	    if msg is None :
		print(cam, " not returned data")
		continue
	    w = msg[0]
	    h = msg[1]
	    c = msg[2]
	    data = msg[6]
	    ba = str(bytearray(data))

            # 2
            ### TIME PROFILE
            interval = time.time() - start
            interval_count += 1
            #print("{} to {} : {}".format(interval_count-1, interval_count,interval))
            ### TIME PROFILE

	    nparr = np.fromstring(ba, np.uint8)
	    img_np = nparr.reshape((h, w, c))
	    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # 3
            ### TIME PROFILE
            interval = time.time() - start
            interval_count += 1
            #print("{} to {} : {}".format(interval_count-1, interval_count,interval))
            ### TIME PROFILE

	    #self.pio.vision.video.setResolution(self.pio.vision.rgb_top, 2)
            #cv2.imshow('window',img_np)
	    cv2.imwrite(face_dir_path+"tmp/1.jpg", img_np)

            # 4 
            ### TIME PROFILE
            interval = time.time() - start
            interval_count += 1
            #print("{} to {} : {}".format(interval_count-1, interval_count,interval))
            ### TIME PROFILE

            # We must do something with 'Path' 
            unknown_picture = img_np
            #unknown_picture = face_recognition.load_image_file(face_dir_path+"tmp/1.jpg")
            unknown_face_encoding = face_recognition.face_encodings(unknown_picture)

            # 5
            ### TIME PROFILE
            interval = time.time() - start
            interval_count += 1
            #print("{} to {} : {}".format(interval_count-1, interval_count,interval))
            ### TIME PROFILE

            if not unknown_face_encoding :
                print("Face not detected")
                continue

            unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

            # 6
            ### TIME PROFILE
            interval = time.time() - start
            interval_count += 1
            #print("{} to {} : {}".format(interval_count-1, interval_count,interval))
            ### TIME PROFILE
            print("Pass")
            print(len(face_list))
            for face in face_list :
                results = face_recognition.compare_faces([face['face_encoding']], unknown_face_encoding,0.3)
                print(results)
                print(frame_no)

                # 7
                ### TIME PROFILE
                interval = time.time() - start
                interval_count += 1
                print("{} to {} : {}".format(interval_count-1, interval_count,interval))
                ### TIME PROFILE

                frame_no +=1
                if results[0] == True :
                    srv['tts'].say("안녕하세요! {}님".format(face['name']))
                    print("True")
                else :
                    print("False")
                    pass



	    cv2.waitKey(1)

    #
    # # Now we can see the two face encodings are of the same person with `compare_faces`!
    #
    #
        



def cam_rgb_test(srv,camera_id = 0) :
    srv['video'] = session.service("ALVideoDevice")

# def get_rgb(self, resolution=None, save_path=None):
    """return current RGB image from camera (top camera)"""

    srv['video'].unsubscribe('jesnk_test')
    rgb_top = srv['video'].subscribeCamera('jesn_test4',0,4,11,1) #name, idx, resolution,colorspace, fps
    rgb_low = srv['video'].subscribeCamera('jesn_test5',1,4,11,1) #name, idx, resolution,colorspace, fps
    depth = srv['video'].subscribeCamera('jesn_test3',2,4,11,1) #name, idx, resolution,colorspace, fps

    cams = []
    cams.append(rgb_top)
    cams.append(rgb_low)
    cams.append(depth)

    #srv['video'].setResolution(rgb_top,4)
    print(srv['video'].getCameraIndexes())
    
    cv2.namedWindow('window', cv2.WINDOW_AUTOSIZE)
    
    file_no = 200
    while (True):
	for cam in cams :
	    msg = srv['video'].getImageRemote(cam)
	    if msg is None :
		print(cam, " not returned data")
		continue
	    w = msg[0]
	    h = msg[1]
	    c = msg[2]
	    data = msg[6]
	    ba = str(bytearray(data))

	    nparr = np.fromstring(ba, np.uint8)
	    img_np = nparr.reshape((h, w, c))
	    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

	    #self.pio.vision.video.setResolution(self.pio.vision.rgb_top, 2)
	    cv2.imshow('window',img_np)
	    cv2.imwrite("/home/jesnk/img/"+str(cam)+"_"+str(file_no) + ".jpeg", img_np)
	    print(cam," ",file_no, " is saved")
	    file_no += 1
	    cv2.waitKey(1)

    return img_np





