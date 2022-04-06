import requests
from flask_server import *
from bot_vars import *

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
from random import randint
from urllib.parse import quote

def return_requests(URL):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'})
    r = s.get(URL, allow_redirects=True)
    cookies = dict(r.cookies)
    # print("cookies -", cookies)
    r = s.post(r.url, allow_redirects=True, verify=False, cookies=cookies)
    return r

def kill_chrome():
    try:
        os.system("pkill chrome")
    except:
        print(traceback.format_exc())

def return_pccomponentes_page(URL):
    actual_URL = URL
    try:
        os.remove(SCRAPING_BY_CHROME_DONE_FILE_PATH)
    except Exception as e:
        # print(str(e))
        pass

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
            # start_server(URL)
            time.sleep(3)
            # webbrowser.get('/usr/bin/google-chrome %s %U --no-sandbox').open(URL)
            # os.system("google-chrome-stable --no-sandbox '" + URL + "'")

            file_name = str(time.ctime()).replace(" ", "_").replace(":", "-") + ".json"
            URL = quote(URL, safe=":/?=&")
            SCRAPPED_FILE_PATH = os.path.join(SCRAPPED_DATA_FILES_PATH, file_name)
            write_current_url(URL, file_name)
            print(URL)
            subprocess.Popen(str("google-chrome-stable --no-sandbox " + URL + "").split(" "))
            time.sleep(1)

            seconds_spent = 0
            retry_scraping = False
            while 1:
                # print("\n\nIf file exits:", os.path.isfile(SCRAPPED_FILE_PATH), "\n\n")
                if os.path.isfile(SCRAPPED_FILE_PATH) == False:
                    time.sleep(3)
                    seconds_spent += 3
                    if seconds_spent > SCRAPPING_MAX_TIMEOUT:
                        retry_scraping = True
                        break
                else:
                    time.sleep(2)
                    break

            if retry_scraping == True:
                kill_chrome()
                try:
                    r = requests.get("http://127.0.0.1:5699/shutdown")
                    print(r.text)
                except Exception as e:
                    print(str(e))
                    # print(traceback.format_exc())
                try:
                    time.sleep(1)
                    server.terminate()
                    server.join()
                except:
                    print(traceback.format_exc())
                    time.sleep(1)
                    # continue

            try:
                r = requests.get("http://127.0.0.1:5699/shutdown")
                print(r.text)
            except Exception as e:
                print(str(e))
                # print(traceback.format_exc())

            try:
                time.sleep(1)
                server.terminate()
                server.join()
            except:
                print(traceback.format_exc())

            time.sleep(2)
            tries = 1
            data = {}
            while tries <= 3:
                try:
                    with open(SCRAPPED_FILE_PATH, 'r') as f:
                        data = json.load(f)
                    break
                except Exception as e:
                    print(str(e))
                    time.sleep(1)
                    tries += 1

            # try:
            #     os.remove(SCRAPPED_FILE_PATH)
            # except Exception as e:
            #     print(str(e))

            # os.remove(SCRAPPED_DATA_JSON_FILE_PATH)
            html_data = data['html']

            return html_data
        except:
            pass

def scrape_pccomponentes_search_page(query, max_price):
    # Ordering by price (lower to upper)
    URL = f"https://www.pccomponentes.com/api-v1/products/search?query={query}&sort=price_asc&channel=es&page=1&pageSize=40&price_to={max_price}"
    URL = f"https://www.pccomponentes.com/buscar/?query={query}&price_to={max_price}&or-price_asc"

    html_data = return_pccomponentes_page(URL)
    soup = BeautifulSoup(html_data, 'html.parser')
    all_product_data = soup.findAll('a',{"data-price": True})
    all_product_data_json = []

    for item in all_product_data:
        data = {
                "product_link": "N/A",
                "product_name": "N/A",
                "product_price": "N/A",
                "product_img_link": "N/A",
                "product_category": "N/A",
                "product_availability": "N/A"
            }
        data['product_link'] = item.get("href")
        data['product_name'] = item.get("data-name")
        data['product_price'] = item.get("data-price")
        data['product_img_link'] = item.findAll("img")[0].get("src")
        data['product_category'] = item.get("data-category")
        data['product_availability'] = item.get("data-availability")
        all_product_data_json.append(data)
    
    return all_product_data_json


        
if __name__ == "__main__":
    RUs = []
    with open(RUNTIME_URLS_FILE_PATH, "w") as f:
        json.dump(RUs, f)
    print(scrape_pccomponentes_search_page("rtx 3060", 400))