import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import gzip
import os
def gps_url():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    gps_html = requests.get('https://celestrak.com/GPS/almanac/SEM/2021/',headers=headers)
    soup = BeautifulSoup(gps_html.text, 'lxml')
    gps_content = soup.select('a[href^="/GPS/almanac/SEM/2021/almanac.sem.week"]')
    gps_url = 'https://celestrak.com'+ gps_content[-1]['href']
    resource = requests.get(gps_url, stream=True)
    with open("./text/gps.text", mode="wb") as fh:
        for chunk in resource.iter_content(chunk_size=100):
            fh.write(chunk)
    return


#gps_url()
def gz():
    chromeOptions = webdriver.ChromeOptions()
    #下载压缩包的路径    绝对路径666
    prefs={'download.default_directory': '/Users/lucky/PycharmProjects/pythonProject/'}
    chromeOptions.add_experimental_option('prefs',prefs)
    #chromeOptions.add_argument('--headless')
    #chromeOptions.add_argument('--disable-gpu')
    driver=webdriver.Chrome(options=chromeOptions,executable_path='./chromedriver')
    driver.implicitly_wait(30)  # 隐性等待，最长等30秒
    driver.get('https://cddis.nasa.gov/archive/gnss/data/daily/2021/brdc/')


    driver.find_element_by_xpath('//*[@id="username"]').send_keys("luckyY1")

    driver.find_element_by_xpath('//*[@id="password"]').send_keys("990424gU")
    driver.find_element_by_xpath(('//*[@class="eui-btn--round eui-btn--green"]')).click()
    time.sleep(20)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    content = soup.select('.archiveItemText')
    con = content[-1]['href'].rstrip()
    gps_url2= 'https://cddis.nasa.gov/archive/gnss/data/daily/2021/brdc/' + content[-1]['href']
    driver.get(gps_url2)
    time.sleep(10)
    driver.close()
    #print(type(con))
    path = 'brdc0740.21n.txt'
    if os.path.exists(path):
        os.remove(path)
    with gzip.open(con, "rb") as f_in:
        with open("brdc0740.21n.txt", "wb")as f_out:
            f_out.write(f_in.read())


    os.remove(con)
    driver.quit()

# 调用 函数


while True:
  gps_url()
  gz()
  time.sleep(1800) # 每隔半小时执行一次



