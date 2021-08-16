from naoqi import ALProxy
from motion import entertain, music_motion


PATH = {"disco": "UrbanStreet.mp3", "bang": "", "guitar": "", "saxophone": "epicsax.ogg"}
BASE_PATH = "/opt/aldebaran/www/apps/bi-sound/"


class Play:
    def __init__(self, srv, mode, ip):
        self.srv = srv
        self.mode = mode
        self.path = BASE_PATH + PATH[self.mode]
        self.ip = ip

    def motion(self):
        pass


class Dance(Play):
    def __init__(self, srv, mode, ip):
        Play.__init__(self, srv, mode, ip)
        self.modes = ["disco", "bang"]

    def motion(self):
        modes = self.modes
        mode = self.modes

        player = ALProxy("ALAudioPlayer", self.ip, 9559)
        player.post.playFileFromPosition(self.path, 0)
        if mode == modes[0]:
            entertain.disco(self.srv)
        elif mode == modes[1]:
            entertain.bang(self.srv)
        player.post.stopAll()


class Music(Play):
    def __init__(self, srv, mode, ip):
        Play.__init__(self, srv, mode, ip)
        self.modes = ["guitar", "saxophone"]

    def motion(self):
        modes = self.modes
        mode = self.mode

        player = ALProxy("ALAudioPlayer", self.ip, 9559)
        player.post.playFileFromPosition(self.path, 0)
        if mode == modes[0]:
            music_motion.guitar(self.srv)
        elif mode == modes[1]:
            music_motion.saxophone(self.srv)
        player.post.stopAll()
