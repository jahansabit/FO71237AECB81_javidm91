#import requests
#import cfscrape
import datetime
from inspect import trace
import pytz
import webbrowser
from bs4 import BeautifulSoup
from amazon.page import ama_doc
from aussar.page import aus_doc
from neobyte.page import neo_doc
from casemod.page import cas_doc
from pccomponentes.page import pcc_doc
import requests
import os
import subprocess
import traceback
from multiprocessing import Process
from flask_server import *
from bot_vars import *

def kill_chrome():
    try:
        os.system("pkill chrome")
    except:
        traceback.print_exc()

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
            # subprocess.Popen(str("google-chrome-stable --no-sandbox --log-level=3 " + URL).split(" "))
            subprocess.Popen(str("google-chrome-stable --no-sandbox " + URL).split(" "))
            time.sleep(1)

            seconds_spent = 0
            retry_scraping = False
            while 1:
                # print("\n\nIf file exits:", os.path.isfile(SCRAPPED_DATA_JSON_FILE_PATH), "\n\n")
                if os.path.isfile(SCRAPPED_DATA_JSON_FILE_PATH) == False:
                    time.sleep(3)
                    seconds_spent += 3
                    if seconds_spent > SCRAPPING_MAX_TIMEOUT:
                        retry_scraping = True
                        break
                else:
                    break
            
            if retry_scraping == True:
                kill_chrome()
                try:
                    r = requests.get("http://127.0.0.1:5699/shutdown")
                    print(r.text)
                except:
                    traceback.print_exc()
                try:
                    time.sleep(1)
                    # server.terminate()
                    server.join()
                except:
                    traceback.print_exc()
                    time.sleep(1)
                    continue
            
            try:
                r = requests.get("http://127.0.0.1:5699/shutdown")
                print(r.text)
            except:
                traceback.print_exc()

            try:
                time.sleep(1)
                # server.terminate()
                server.join()
            except:
                traceback.print_exc()
            
            with open(SCRAPPED_DATA_JSON_FILE_PATH, 'r') as f:
                data = json.load(f)
            
            # os.remove(SCRAPPED_DATA_JSON_FILE_PATH)
            html_data = data['html']

            soup = BeautifulSoup(html_data, 'html.parser')

            try:
                product_name = soup.h1.strong.get_text()
            except:
                product_name = str(soup.find('title').get_text()).replace("| PcComponentes.com", "").strip()
            product_price = soup.findAll(id="precio-main")[0].get("data-price")
            product_img_link = soup.findAll('div',{"class":"item badgets-layer"})[0].a.get("href")
            if "https:" not in product_img_link:
                product_img_link = "https:" + product_img_link
            product_micro_data = json.loads(str(soup.findAll('script',{"id":"microdata-product-script"})[0].get_text()))
            # pprint(product_micro_data)
            try:
                availability = str(product_micro_data['offers']['availability']).replace("http://schema.org/", "")
            except:
                availability = str(product_micro_data['offers']['offers']['availability']).replace("http://schema.org/", "")

            try:
                product_category = soup.findAll('a',{"class":"GTM-breadcumb"})[2].get_text()
            except:
                traceback.print_exc()
                product_category = ""

            return {
                "product_link": URL,
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link,
                "product_category": product_category,
                "product_availability": availability
            }
        except Exception as e:
            print("\n\n")
            traceback.print_exc()
            print("\n\n")
            print(e)
            kill_chrome()
            time.sleep(3)
            return None

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
                "product_link": URL,
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
                "product_link": URL,
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
                "product_link": URL,
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
        response_status = 404
        try:
            r = return_requests(URL)
            # r = requests.get(URL)
            # with open("coolmod.html", "wb") as f:
            #     f.write(r.content)
            response_status = r.status_code
            print(response_status)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            product_name = soup.findAll("div", {"class": "productTitle"})[0].get_text()
            product_price = str(soup.findAll("span", {"id":"normalpricenumber"})[0].get_text()).replace(",", ".")
            if product_price.count(".") <= 2:
                product_price = product_price.replace(".", "", product_price.count(".") - 1)
            product_img_link = soup.find("img", {"id":"productmainimageitem"}).get('src')
            # availability = soup.findAll("span", {"id":"messageStock"})[0].get_text() # usable for selenium

            # Avalability Checker
            product_id = str(soup.findAll("div", {"class":"productextrainfotext"})[1].get_text()).strip()
            CatId = soup.find("input", {"id":"subfamily"}).get('value')
            TarId = 1
            DayId = "AM"
            
            spain_timezone = pytz.timezone('Europe/Madrid')
            datetime_obj = datetime.now(spain_timezone)
            hour = datetime_obj.hour
            if hour >= 12:
                DayId = "PM"
            
            r = return_requests(f"https://www.coolmod.com/view/ajax/category/ajaxPricesForProducts.php?CatId={CatId}&TarId={TarId}&DayId={DayId}")
            products_data = r.json()

            for product in products_data:
                if product['ProducCode'] == product_id: # Yeah, I know. It is ProducCode, without a 't'.
                    if product['TextDelivered'].lower() == "agotado":
                        availability = "OutOfStock"
                    else:
                        availability = "InStock"
                    break
            

            return {
                "product_link": URL,
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link,
                "product_availability": availability
            }
        except Exception as e:
            traceback.print_exc()
            print(e)
            time.sleep(3)
            print(f"Response Status: {response_status}")
            if (response_status >= 200 and response_status < 300):
                pass
            else:
                return None

def get_from_aussar(URL):
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
            
            product_name = soup.findAll("h1", {"class": "product-detail-name"})[0].get_text()
            product_price = str(soup.findAll("div", {"class":"current-price"})[0].span.get("content"))
            product_img_link = soup.find("img", {"class":"product-cover-modal"}).get('src')

            return {
                "product_link": URL,
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link
            }
        except Exception as e:
            print(e)
            time.sleep(3)


if __name__ == "__main__":
    # print(get_from_pccomponentes("https://www.pccomponentes.com/gigabyte-radeon-rx-6700-xt-eagle-oc-12gb-gddr6-reacondicionado"))
    # print(get_from_pccomponentes("https://www.pccomponentes.com/asus-tuf-gaming-geforce-gtx-1660-super-oc-edition-6gb-gddr6"))
    print(get_from_coolmod("https://www.coolmod.com/razer-blade-17-d17-7nt-i7-11800h-rtx-3070-16gb-1tb-17-3/"))
