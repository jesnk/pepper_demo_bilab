# -*- encoding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import sys

sys.path.insert(0, './speech_recognition')
import audio


class saju(object):
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


def calculate(value):
    print("calculate:", value)
    # value가 '1998 December 10th Female' 이라고 가정하면
    rem = value.translate({ord(i): None for i in 'th'})
    sent = rem.split()

    mon = sent[1]
    if mon == 'January':
        month = '1'
    elif mon == 'February':
        month = '2'
    elif mon == 'March':
        month = '3'
    elif mon == 'April':
        month = '4'
    elif mon == 'May':
        month = '5'
    elif mon == 'June':
        month = '6'
    elif mon == 'July':
        month = '7'
    elif mon == 'August':
        month = '8'
    elif mon == 'September':
        month = '9'
    elif mon == 'October':
        mon = '10'
    elif mon == 'November':
        month = '11'
    if mon == 'December':
        month = '12'

    if "여자" or "female" in value:
        gen = 2
    elif '남자' or 'male' in value:
        gen = 1

    gender = "% s" % gen
    year = sent[0]
    # month = sent[1]
    day = sent[2]
    return gender, year, month, day


def main(srv):
    print("2021 saju mode")
    srv['tts'].say("Hello!")

    value = audio.get_string()
    gender, year, month, day = calculate(value)

    year = '2021'  # 2021
    gender = gender  # 1:male, 2:female
    birth_year = year  # '1994'
    birth_month = month  # '04'
    birth_day = day  # '11'

    birth_hour = 'N'  # default is N
    solun = '01'  # 양력
    lun_yn = '01'  # 평달
    url = 'http://tojung.freeunse.funstory.biz/sub/tradition4.php?unse_yy=' + year + '&unse1_sex=' + gender + '&unse1_yy=' + birth_year + '&unse1_mm=' + birth_month + '&unse1_dd=' + birth_day + '&unse1_hh=' + birth_hour + '&unse1_solun=' + solun + '&unse1_lun_yn=' + lun_yn
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    my_titles = soup.select('.box_1111')
    response = my_titles[0].text
    print(response)
    return response
