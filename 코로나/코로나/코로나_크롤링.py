import time
import string
import datetime
import csv
from ckonlpy.tag import Twitter
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome("c:/Users/yooat/Downloads/chromedriver/chromedriver")

driver.get('http://www.cheonan.go.kr/covid19/sub02_01.do')
time.sleep(1)
twitter = Twitter()
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
name = soup.find_all("dl",class_="item")
f1 = open('corona.txt','w+t')

for test in name:
    if  "14일이" in test.get_text():
        continue
    f1.write(test.get_text() + "\n")
f1.close();

f1 = open('corona.txt','r')
nowDate = datetime.datetime.now()
c = csv.writer(open(nowDate.strftime("result_" + "%Y-%m-%d_%H-%M-%S") + ".csv","w",encoding="cp949"))
for l in f1:
    c.writerow(twitter.nouns(l))
time.sleep(3)