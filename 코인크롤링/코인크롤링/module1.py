from tkinter import *
import tkinter.messagebox
import string
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from threading import Thread
import time

options = Options()
options.add_argument("--headless")
options.add_argument("disable-gpu")
driver = webdriver.Firefox(options=options, executable_path="C:\\Users\\yooat\\Downloads\\geckodriver-v0.26.0-win64\\geckodriver.exe")
site = " "
name = " "
price = " "
root = Tk()
root.title("코인알리미")
root.geometry("400x500+100+100")
root.resizable(False,False)

lb1 = Label(root, text = "코인거래소 주소를 붙혀주세요 : ")
lb1.place(x=10,y = 10)
txt1 = Entry(root)
txt1.place(x = 190, y = 10)
def function_btn1():
    global site 
    site = txt1.get()
    driver.get(site)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    name = str(soup.find("div",class_="asset-name"))
    name = re.sub('<.+?>', '', name, 0).strip()
    price = str(soup.find("div",class_="close-price RISE"));
    price = re.sub('<.+?>', '', price, 0).strip()
    price = re.sub('KRW', '', price, 0).strip()
    price = price.replace(",","");
    txt2.insert(0,name);
    txt3.insert(0,price);
btn1 = Button(root,text = "OK",command = function_btn1)
btn1.place(x=340,y=10)

lb2 = Label(root, text = "코인 이름 : ")
lb2.place(x=10,y = 50)
txt2 = Entry(root)
txt2.place(x = 80, y = 50)

lb3 = Label(root, text = "코인 초기 가격 : ")
lb3.place(x = 10, y = 90)
txt3 = Entry(root)
txt3.place(x = 110, y = 90)

over = " "
under = " "

lb4 = Label(root, text = "상한가 설정 : ")
lb4.place(x=10,y = 130)
txt4 = Entry(root)
txt4.place(x = 110, y = 130)

lb5 = Label(root, text = "하한가 설정 : ")
lb5.place(x=10,y = 170)
txt5 = Entry(root)
txt5.place(x = 110, y = 170)

lb6 = Label(root, text = "설정된 상,하한가 : ")
lb6.place(x = 10, y = 210)
txt6 = Entry(root)
txt6.place(x = 130, y = 210)
def function_button6():
    global over, under
    over = txt4.get()
    under = txt5.get()
    tmp = under + " < x < " + over
    txt6.insert(0,tmp)
    
btn6 = Button(root,text = "OK",command = function_button6)
btn6.place(x=260,y=170)

lb7 = Label(root, text = "-----변동가격 표시-----")
lb7.place(x = 10, y = 250)
txt7 = Text(root,height = 20)
txt7.place(x = 10, y = 280)
def m_thread(val):
    global under, over
    i = 0
    while True:
        driver.get(site)
        time.sleep(2)
        html = driver.page_source;
        soup = BeautifulSoup(html, "html.parser")
        price = str(soup.find("div",class_="close-price RISE"));
        price = re.sub('<.+?>', '', price, 0).strip()
        price = re.sub('KRW', '', price, 0).strip()
        price = price.replace(",","");
        if i == 10:
            txt7.delete("1.0","end")
            i = 0
        txt7.insert(tkinter.CURRENT, "현재가격 : " + price + "\n")
        i = i + 1
        if int(price) <= int(under):
            tkinter.messagebox.showinfo("떡락","떡락합니다!!!!!!\n칼손절하세요!!!!!!!")
            break
        if int(price) >= int(over):
            tkinter.messagebox.showinfo("떡상","떡상합니다!!!!!!\n꽉잡으세요!!!!!!!")
            break
        time.sleep(10)
t = Thread(target = m_thread, args=(1,))
def function_button7():
    t.start()
btn7 = Button(root,text = "서치시작", command = function_button7)
btn7.place(x = 170, y = 240)


def on_closing():
    if tkinter.messagebox.askokcancel("종료", "진짜 종료하실거에요?"):
        driver.quit()
        root.destroy()
root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()