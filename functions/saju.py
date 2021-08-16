# -*- encoding: UTF-8 -*-

from speech import audio
import requests
from bs4 import BeautifulSoup
import sys

# insert the path
# sys.path.insert(0, './speech')


class saju:
    def __init__(self, srv):
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


class Translate:

    months = {"January": 1, "Fabuary": 2, "March": 3, "April": 4, "May": 5, "June": 6,
              "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

    def __init__(self):
        pass

    def calculate(self, value):
            # print("calculate:", value)  # for debugging
            # if value == '1998 December 10th Female', then
            rem = value.translate({ord(i): None for i in 'th'})
            sent = rem.split()

            mon = sent[1]
            if mon in self.months.keys():
                month = str(self.months[mon])
            else:
                return None

            if "여자" or "female" in value:
                gender = "2"
            elif '남자' or 'male' in value:
                gender = "1"
            else:
                return None

            year = sent[0]
            day = sent[2]

            return gender, year, month, day

    # to create the string of URL address
    def make_url(self, gender, year, birth_year, month, day):
        solun = '01'  # 양력
        lun_yn = '01'  # 평달
        birth_hour = "N"  # default value
        url = 'http://tojung.freeunse.funstory.biz/sub/tradition4.php?unse_yy=' + year \
              + '&unse1_sex=' + gender + '&unse1_yy=' + birth_year + '&unse1_mm=' + month \
              + '&unse1_dd=' + day + '&unse1_hh=' + birth_hour + '&unse1_solun=' + solun \
              + '&unse1_lun_yn=' + lun_yn
        return url


# main function
def main(srv):
    print("2021 saju mode")
    srv['tts'].say("Hello!")

    translate = Translate()  # class for make url with the answer

    value = audio.get_string()
    try:
        calculated = translate.calculate(value)
        if calculated is None:
            raise ValueError
    except ValueError:
        response = "Invalid command. Try again."
        return response

    # make URL address
    gender, birth_year, birth_month, birth_day = calculated
    current = '2021'  # 2021
    url = translate.make_url(gender, current, birth_year, birth_month, birth_day)

    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    my_titles = soup.select('.box_1111')
    response = my_titles[0].text
    # print(response)  # for debugging
    return response
