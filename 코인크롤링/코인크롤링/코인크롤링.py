import string
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from tkinter import *
import tkinter.messagebox


def function_price():
    price = str(soup.find("div", class_="close-price RISE"))
    price = re.sub('<.+?>', '', price, 0).strip()
    price = re.sub('KRW', '', price, 0).strip()
    price = price.replace(",", "")
    return price


options = Options()
options.add_argument("--headless")
options.add_argument("disable-gpu")
driver = webdriver.Firefox(options=options, executable_path="C:\\Users\\yooat\\Downloads\\geckodriver.exe")

print("찾는 코인 URL을 붙혀주세요(코인빗) : ")
site = input()
driver.get(site)
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

name = str(soup.find("div", class_="asset-name"))
name = re.sub('<.+?>', '', name, 0).strip()
price = function_price()

print("현재 " + name + "의 가격은 " + price + " 입니다")
print("원하는 상한가와 하한가를 설정해 주세요 : ")
over, under = input().split()
print("상한가 " + over + "와 하한가 " + under + "도달시 알려드립니다.")

while True:
    driver.get(site)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    price = function_price()
    print("현재 가격 : " + price + "\n")
    if int(price) <= int(under):
        tkinter.messagebox.showinfo("떡락", "떡락합니다!!!!!!\n칼손절하세요!!!!!!!")
        break
    if int(price) >= int(over):
        tkinter.messagebox.showinfo("떡상", "떡상합니다!!!!!!\n꽉잡으세요!!!!!!!")
        break
    time.sleep(15)

driver.quit()
