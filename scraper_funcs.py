#import requests
#import cfscrape
import webbrowser
from bs4 import BeautifulSoup
from amazon.page import ama_doc
from neobyte.page import neo_doc
from casemod.page import cas_doc
from pccomponentes.page import pcc_doc
import requests
import os
import subprocess
from multiprocessing import Process
from flask_server import *
from bot_vars import *

def kill_chrome():
    try:
        os.system("pkill chrome")
    except:
        pass

def return_requests(URL):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'})
    r = s.get(URL)
    cookies = dict(r.cookies)
    # print("cookies -", cookies)
    r = s.post(URL, verify=False, cookies=cookies)
    return r

def get_from_pccomponentes(URL):
    RETRY_COUNT = -1
    while 1:
        RETRY_COUNT += 1
        if RETRY_COUNT > SCRAPING_MAX_RETRIES:
            return None
        try:
            try:
                os.remove(SCRAPPED_DATA_JSON_FILE_PATH)
            except:
                pass

            server = Process(target=start_server)
            server.start()
            time.sleep(1)
            # webbrowser.get('/usr/bin/google-chrome %s %U --no-sandbox').open(URL)
            # os.system("google-chrome-stable --no-sandbox '" + URL + "'")
            subprocess.Popen(str("google-chrome-stable --no-sandbox " + URL).split(" "))
            time.sleep(1)
            while 1:
                print("\n\nIf file exits:", os.path.isfile(SCRAPPED_DATA_JSON_FILE_PATH), "\n\n")
                if os.path.isfile(SCRAPPED_DATA_JSON_FILE_PATH) == False:
                    time.sleep(3)
                else:
                    break
            
            time.sleep(1)
            server.terminate()
            server.join()
            
            with open(SCRAPPED_DATA_JSON_FILE_PATH, 'r') as f:
                data = json.load(f)
            
            os.remove(SCRAPPED_DATA_JSON_FILE_PATH)
            html_data = data['html']

            soup = BeautifulSoup(html_data, 'html.parser')

            product_name = soup.h1.strong.get_text()
            product_price = soup.findAll(id="precio-main")[0].get("data-price")
            product_img_link = soup.findAll('div',{"class":"item badgets-layer"})[0].a.get("href")

            return {
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link":product_img_link
            }
        except Exception as e:
            print(e)
            kill_chrome()
            time.sleep(3)

def get_from_neobyte(URL):
    RETRY_COUNT = -1
    while 1:
        RETRY_COUNT += 1
        if RETRY_COUNT > SCRAPING_MAX_RETRIES:
            return None
        try:
            r = return_requests(URL)
            # r = requests.get(URL)
            # with open("neobyte.html", "wb") as f:
            #     f.write(r.content)

            soup = BeautifulSoup(r.content, 'html.parser')

            product_name = soup.title.get_text()
            product_price = soup.findAll(itemprop="price")[0].get('content')
            product_img_link = soup.findAll('div',{"class":"easyzoom easyzoom-product"})[0].a.get("href")

            return {
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link
            }
        except Exception as e:
            print(e)
            time.sleep(3)

def get_from_casemod(URL):
    RETRY_COUNT = -1
    while 1:
        RETRY_COUNT += 1
        if RETRY_COUNT > SCRAPING_MAX_RETRIES:
            return None
        try:
            r = return_requests(URL)
            # r = requests.get(URL)
            # with open("neobyte.html", "wb") as f:
            #     f.write(r.content)

            soup = BeautifulSoup(r.content, 'html.parser')

            product_name = soup.title.get_text()
            product_price = soup.findAll(itemprop="price")[0].get('content')
            product_img_link = soup.find("div", {"id": "product-images-large"}).img.get('content')

            return {
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link
            }
        except Exception as e:
            print(e)
            time.sleep(3)

def get_from_amazon(URL):
    RETRY_COUNT = -1
    while 1:
        RETRY_COUNT += 1
        if RETRY_COUNT > SCRAPING_MAX_RETRIES:
            return None
        try:
            r = return_requests(URL)
            # r = requests.get(URL)
            # with open("neobyte.html", "wb") as f:
            #     f.write(r.content)

            soup = BeautifulSoup(r.content, 'html.parser')
            
            product_name = ' '.join([word for word in (soup.findAll(id="productTitle")[0].get_text()).split() if word != " "])
            product_price = soup.findAll("span", {"data-a-color":"price"})[0].get_text()[:6]
            product_img_link = soup.find("div", {"id":"imgTagWrapperId"}).img.get('src')

            return {
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link
            }
        except Exception as e:
            print(e)
            time.sleep(3)

def get_from_coolmod(URL):
    RETRY_COUNT = -1
    while 1:
        RETRY_COUNT += 1
        if RETRY_COUNT > SCRAPING_MAX_RETRIES:
            return None
        try:
            r = return_requests(URL)
            # r = requests.get(URL)
            # with open("coolmod.html", "wb") as f:
            #     f.write(r.content)

            soup = BeautifulSoup(r.content, 'html.parser')
            
            product_name = soup.findAll("div", {"class": "productTitle"})[0].get_text()
            product_price = str(soup.findAll("span", {"id":"normalpricenumber"})[0].get_text()).replace(",", ".")
            product_img_link = soup.find("img", {"id":"productmainimageitem"}).get('src')

            return {
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link
            }
        except Exception as e:
            print(e)
            time.sleep(3)


if __name__ == "__main__":
    print(get_from_coolmod("https://www.coolmod.com/msi-geforce-gtx-1660-super-ventus-xs-oc-6gb-gddr6-tarjeta-grafica/"))
