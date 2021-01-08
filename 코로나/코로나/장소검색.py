from selenium import webdriver
import time
import re
import json
from bs4 import BeautifulSoup

driver = webdriver.Chrome("d:\chromedriver.exe")


def crawl_ra(rn):
    jsonData = {}
    jsonData["name"] = rn
    driver.get("https://map.naver.com/v5/search/" + rn)
    time.sleep(2)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="searchIframe"]'))

    try:
        driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/div[1]/a/span[1]').click()
    except:
        try:
            driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[2]/div[1]/a/span[1]').click()
        except:
            try:
                driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[2]/div[1]/a/span[3]').click()
            except:
                driver.refresh()

    driver.switch_to_default_content()
    time.sleep(2)
    iframes = driver.find_elements_by_tag_name('iframe')
    driver.switch_to.frame(iframes[-1])

    page_source = driver.page_source

    try:
        address = driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[4]/div/div[2]/div/ul/li[2]/div/span[1]').text
    except:
        try:
            address = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[4]/div/div[1]/div/ul/li[2]/div/span[1]').text
        except:
            try:
                address = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[4]/div/div[1]/div/ul/li/div/span[1]').text
            except:
                address = "null"
    jsonData["address"] = address

    try:
        phone = re.findall('\d{0,3}-\d{3,4}-\d{4}', page_source)[0]
    except:
        phone = "null"
    jsonData["phone"] = phone
    foods = []

    pas = False
    for i in range(1, 100):
        try:
            food_name_path = """/html/body/div[3]/div/div[2]/div[4]/div/div[2]/div[1]/ul/li[%d]/div/div/span/span""" % (i)
            food_price_path = """/html/body/div[3]/div/div[2]/div[4]/div/div[2]/div[1]/ul/li[%d]/div/em""" % (i)
            foods.append({"name": driver.find_element_by_xpath(food_name_path).text, "price": driver.find_element_by_xpath(food_price_path).text})
        except Exception as ex:
            if i == 1:
                pas = True
            break

    if pas == True:
        for i in range(1, 100):
            try:
                food_name_path = """/html/body/div[3]/div/div[2]/div[4]/div/div[3]/div[1]/ul/li[%d]/div/div/span/span""" % (i)
                food_price_path = """/html/body/div[3]/div/div[2]/div[4]/div/div[3]/div[1]/ul/li[%d]/div/em""" % (i)
                foods.append({"name": driver.find_element_by_xpath(food_name_path).text, "price": driver.find_element_by_xpath(food_price_path).text})
            except Exception as ex:
                if i == 1:
                    foods.append({"name": "null", "price": "null"})
                break

    jsonData["food"] = foods

    try:
        gasolin = re.findall("휘발유.*?원", page_source)[0].replace(",", "")
        gasolin = re.findall("\d+", gasolin)[0]
    except:
        gasolin = "X"
    try:
        disel = re.findall("경유.*?원", page_source)[0].replace(",", "")
        disel = re.findall("\d+", disel)[0]
    except:
        disel = "X"
    try:
        LPG = re.findall("LPG.*?원", page_source)[0].replace(",", "")
        LPG = re.findall("\d+", LPG)[0]
    except:
        LPG = "X"

    jsonData["gasoline"] = gasolin
    jsonData["diesel"] = disel
    jsonData["LPG"] = LPG

    convs = []
    try:
        conv_val = re.findall("편의시설</h3>.*?</ul>", page_source)[0]
        conv_val = re.findall("[가-힣]+", conv_val)
        conv_val = conv_val[1:]
        for i in conv_val:
            convs.append({"name": i})
        jsonData["conv_val"] = convs
    except:
        jsonData["conv_val"] = ["null"]

    print(jsonData)
    return jsonData


with open('test.json', 'r',  encoding='euc-kr') as json_file:
    json_data = json.load(json_file)

data = []
for a in json_data['list']:
    print(a['unitName'])
    data.append(crawl_ra(a['unitName']))

writeInfo = {"data": data}

with open('휴게소.json', 'w', encoding="utf-8") as f:
    json.dump(writeInfo, f, ensure_ascii=False, indent="\t")
