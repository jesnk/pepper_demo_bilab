from random import randint
from speech import audio

# the string of responses
UP = "Up"
DOWN = "Down"
CORRECT = "That's correct!"
ERROR = "Error occurs."  # error statement

# the constant values of the range of the answer
MIN = 1
MAX = 50

# the constant value of trials
TRIAL = 10


class UpDown:
    def __init__(self, srv):
        self.answer = randint(MIN, MAX + 1)
        self.tts = srv['tts']
        self.asr = srv['asr']
        srv['asr'].setLanguage("English")
        self.exit_flag = False

    def asr_callback(self, msg):
        # Threshold
        if msg[1] > 0.4:
            print(msg[0], msg[1], " is returned")
            self.ret['type'] = 'speech'
            self.ret['word'] = msg[0]
            self.exit_flag = True

    def correct(self, number):
        return self.answer == number

    def response(self, number):
        is_right = self.correct(number)
        if is_right:
            return CORRECT
        elif self.answer > number:
            return UP
        elif self.answer < number:
            return DOWN
        return ERROR  # invalid case

    def show_result(self, correct):
        if correct:
            return "You loose."
        return "Exceeded the number of attempts. Game over."

    def play(self):
        tts = self.tts

        # initialization
        correct = False
        count = 0

        tts.say("Hello!")

        while count < TRIAL:
            tts.say("Say the number between %d to %d" % (MIN, MAX))
            value = audio.get_string()
            try:
                if value is audio.INVALID:
                    raise ValueError
                int_value = int(value)
                if int_value not in range(MIN, MAX + 1):
                    raise ValueError
            except ValueError:
                tts.say("Invalid. Try again.")
                continue
            try:
                response = self.response(int_value)
                tts.say(response)
                if response == ERROR:
                    raise RuntimeError
            except RuntimeError:
                return  # the program ends
            correct = self.correct(int_value)  # update the value
            if correct:
                break  # the game ends if the answer is correct
            count += 1

        tts.say(self.show_result(correct))
