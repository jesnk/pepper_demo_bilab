# -*- encoding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

year = '2021' # 2021
gender = '1' #
birth_year = '1994'
birth_month = '04'
birth_day = '29'
birth_hour = 'N' # default is N
solun = '01' # 양력
lun_yn = '01' # 평달
url = 'http://tojung.freeunse.funstory.biz/sub/tradition4.php?unse_yy='+year+'&unse1_sex='+gender+'&unse1_yy='+birth_year+'&unse1_mm='+birth_month+'&unse1_dd='+birth_day+'&unse1_hh='+birth_hour+'&unse1_solun='+solun+'&unse1_lun_yn='+lun_yn
headers = {'User-Agent': 'Mozilla/5.0'}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')
my_titles = soup.select('.box_1111')
print(my_titles[0].text)