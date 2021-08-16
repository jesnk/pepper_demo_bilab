#! /usr/bin/env python
# _*_ encoding: UTF-8 _*_

from naoqi import ALProxy

useSensorValues = False

motion = ALProxy("ALMotion", "192.168.50.188", 9559)
tts = ALProxy("ALTextToSpeech", "192.168.50.188", 9559)
motion.moveInit()
print(motion.getRobotPosition(useSensorValues))
# for idx, num in enumerate([0.5, -0.5]):
#     id = motion.post.moveTo(num, 0, 0)
#     if (idx+1) % 2.0 == 0:
#         tts.say("I'm moving backward")
#         result = motion.getRobotPosition(useSensorValues)
#         print("Position after Move %d" % (idx+1), result)
#         motion.wait(id, 0)
#     else:
#         tts.say("I'm moving forward")
#         result = motion.getRobotPosition(useSensorValues)
#         print("Position after Move %d" % (idx+1), result)
#         motion.wait(id, 0)
#
# for idx, num in enumerate([0.5, -0.5]):
#     id = motion.post.moveTo(0, num, 0)
#     if (idx+1) % 2.0 == 0:
#         tts.say("I'm moving right")
#         result = motion.getRobotPosition(useSensorValues)
#         print("Position after Move %d" % (idx+1), result)
#         motion.wait(id, 0)
#     else:
#         tts.say("I'm moving left")
#         result = motion.getRobotPosition(useSensorValues)
#         print("Position after Move %d" % (idx+1), result)
#         motion.wait(id, 0)
