import requests
import string
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")
options.add_argument("disable-gpu")
driver = webdriver.Firefox(options=options, executable_path="C:\\Users\\yooat\\Downloads\\geckodriver-v0.26.0-win64\\geckodriver.exe")

http = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=10"
page = "#&date=%2000:00:00&page="
tmp1, tmp2 = input("원하는 분야와 페이지를 입력해 주세요 : \n(정치 : 0, 경제 : 1, 사회 : 2, 생활/문화 : 3, 세계 : 4, IT/과학 : 5 | 페이지 입력)").split()
site = http + tmp1 + page + tmp2
driver.get(site)
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

newslink = []
newsaids = []
linksource = soup.find("div",class_ = "content").find_all("a")
for a in linksource :
    if "aid=" in str(a.get('href')):
        snum = (a.get('href').find("aid="))
        newsnum = str(a.get('href'))[snum+4:snum+14]
        if newsnum not in newsaids : 
            newsaids.append(newsnum)
            if str(a.get('href'))[0] != "h":
                newslink.append("https://news.naver.com/" + str(a.get('href')))
            else:
                newslink.append(str(a.get('href')))

driver.quit()
for a in newslink:
    print(a)
for a in newsaids:
    print(a)