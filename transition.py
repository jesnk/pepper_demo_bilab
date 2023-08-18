import time
from naoqi import ALProxy

from data_list import *
# from cameras import take_photo
# from functions import updown, saju
from functions.play_music import *


aas_configuration = {"bodyLanguageMode": "contextual"}


class Transition:
    def __init__(self):
        pass

    def get_html_address(self, file_name):
        name = file_name
        if len(name) > 5 and name[-5:] == '.html':
            name = name[:-5]
        return "http://198.18.0.1/apps/bi-html/" + name + '.html'

    def home(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next")
                return SCENES[next_scene]

        elif input_ret['type'] == 'speech':
            if input_ret['word'] == 'start':
                next_scene = 'first_menu'
                srv['aas'].say("Hello, Nice to meet you!", aas_configuration)
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                return SCENES[next_scene]

            elif input_ret['word'] == 'hello':
                print("test")
                next_scene = 'home'
                srv['aas'].say("Hello Sir!", aas_configuration)
                return SCENES[next_scene]

            elif input_ret['word'] == 'pepper':
                next_scene = 'home'
                srv['aas'].say("Yep! Hello?!", aas_configuration)
                return SCENES[next_scene]

            elif input_ret['word'] == 'cheese':
                photo_test = take_photo.Photo(srv)
                photo_test.take()
                pass

        # default value
        # return SCENES['home']

    def first(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_LEFT':
                next_scene = 'tour'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                next_scene = 'entertain'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'first_menu'
                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                srv['aas'].say(
                    "Are you curious about me? I am Pepper. It is a humanoid robot made by Softbank, and can use artificial intelligence. It is characterized by a cute appearance, and is introduced in various fields such as finance, bookstore, medical care, and distribution fields in Korea")
                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                return SCENES[next_scene]

        elif input_ret['type'] == 'speech':
            if input_ret['word'] == 'bye':
                return SCENES['exit']

            elif input_ret['word'] == 'first':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                return SCENES[next_scene]

            elif input_ret['word'] == 'who':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                return SCENES[next_scene]

    def tour(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_RIGHT':
                next_scene = 'tour_hsr1'
                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("Let me explain the robots in our center. First, HSR, a human helper robot, is a mobile operation robot.", aas_configuration)

                next_scene = 'tour_hsr2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("It is about 1 meter tall and is a versatile robot that can recognize objects through various cameras and pick them up with a gripper. But is it ugly than me?",
                               aas_configuration)

                next_scene = 'tour_bigbot'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say(
                    "The next robot, big bot. It is a robot made by combining a base robot, which is specialized in moving objects, and a kinova arm robot that picks up objects. In addition, it is a mobile operation robot that is equipped with sound and camera sensors, capable of recognizing objects and gripping them with a gripper.",
                    aas_configuration)

                next_scene = 'tour_pepper1'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say(
                    "The last robot to be introduced is me, Pepper. I am a humanoid robot made by Softbank, and I can use artificial intelligence.", aas_configuration)

                next_scene = 'tour_pepper2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say(
                    "I have a cute appearance, and has been introduced in various fields such as finance, bookstores, medical care, and distribution fields in Korea. In addition, it is used as a standard robot in S, S, P, L, among the world robot competitions, Robo Cup League.",
                    aas_configuration)

                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                next_scene = 'tour'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                next_scene = 'tour_ourlab1'
                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say(
                    "Let me introduce our lab. Our bio-intelligence lab is conducting the following studies. First, we are conducting interdisciplinary research in various fields such as artificial intelligence, psychology, and cognitive science to develop human-level artificial intelligence such as PEECA and LBA. We are also actively conducting research on robots on various platforms, such as home robots that work with humans and Robocup, a world robot competition.",
                    aas_configuration)

                next_scene = 'tour_ourlab2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("If you have any other questions or inquiries, please refer to the following website or contact us.", aas_configuration)

                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                next_scene = 'tour'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("To the initial screen", aas_configuration)
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'tour'
                srv['tts'].setParameter("defaultVoiceSpeed", 110)
                srv['aas'].say(
                    "Are you curious about me? I am Pepper. It is a humanoid robot made by Softbank, and can use artificial intelligence. It is characterized by a cute appearance, and is introduced in various fields such as finance, bookstore, medical care, and distribution fields in Korea",
                    aas_configuration)
                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                return SCENES[next_scene]

    def entertain(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                file_path = "/opt/aldebaran/www/apps/bi-sound/elephant.ogg"
                # srv['tts'].post.say('yes')
                player = ALProxy("ALAudioPlayer", PEPPER_IP, 9559)
                player.post.playFileFromPosition(file_path, 0)
                entertain.elephant(srv)
                player.post.stopAll()
                pass

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                file_path = "/opt/aldebaran/www/apps/bi-sound/UrbanStreet.mp3"
                # player = Dance(srv, "disco", PEPPER_IP)
                # player.motion()
                print("hello")
                player = ALProxy("ALAudioPlayer", PEPPER_IP, 9559)
                player.post.playFileFromPosition(file_path, 0)
                entertain.disco(srv)
                player.post.stopAll()
                pass

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'entertain2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next")
                return SCENES[next_scene]

    def entertain2(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                srv['aas'].say("Please tell me your date of birth in English.", aas_configuration)
                text = saju.main(srv)
                srv['aas'].say(text, aas_configuration)  # written as "srv['ass']" before

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                srv['tts'].say("You must say the number in English. Other language is not allowed.")
                time.sleep(3)  # wait for 3 seconds
                updown.UpDown(srv).play()

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'entertain'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next")
                return SCENES[next_scene]

    # return the object of the next scene
    def switch(self, srv, scene, input_ret):
        if scene == "home":
            return self.home(srv, input_ret)
        elif scene == "first_menu":
            return self.first(srv, input_ret)
        elif scene == "tour":
            return self.tour(srv, input_ret)
        elif scene == "entertain":
            return self.entertain(srv, input_ret)
        elif scene == "entertain2":
            return self.entertain2(srv, input_ret)
