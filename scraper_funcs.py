#import requests
#import cfscrape
from bs4 import BeautifulSoup
from amazon.page import ama_doc
from neobyte.page import neo_doc
from casemod.page import cas_doc
from pccomponentes.page import pcc_doc
import requests
import os
from multiprocessing import Process
from flask_server import *
from bot_vars import *

def return_requests(URL):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'})
    r = s.get(URL)
    cookies = dict(r.cookies)
    print("cookies -", cookies)
    r = s.post(URL, verify=False, cookies=cookies)
    return r

def get_from_pccomponentes(URL, html_data=None):
    if html_data is None:
        # r = return_requests(URL)
        # # r = requests.get(URL)
        # with open("neobyte.html", "wb") as f:
        #     f.write(r.content)

        server = Process(target=start_server)
        server.start()

        while os.path.isfile(SCRAPPED_DATA_JSON_FILE_PATH) == False:

        
            html_data = r.content

    soup = BeautifulSoup(html_data, 'html.parser')

    product_name = soup.h1.strong.get_text()
    product_price = soup.findAll(id="precio-main")[0].get("data-price")
    product_img_link = soup.findAll('div',{"class":"item badgets-layer"})[0].a.get("href")

    return {
        "product_name": product_name,
        "product_price": product_price,
        "product_img_link":product_img_link
    }

def get_from_neobyte(URL):
    r = return_requests(URL)
    # r = requests.get(URL)
    with open("neobyte.html", "wb") as f:
        f.write(r.content)

    soup = BeautifulSoup(r.content, 'html.parser')

    product_name = soup.title.get_text()
    product_price = soup.findAll(itemprop="price")[0].get('content')
    product_img_link = soup.findAll('div',{"class":"easyzoom easyzoom-product"})[0].a.get("href")

    return {
        "product_name": product_name,
        "product_price": product_price,
        "product_img_link": product_img_link
    }

def get_from_casemod(URL):
    r = return_requests(URL)
    # r = requests.get(URL)
    with open("neobyte.html", "wb") as f:
        f.write(r.content)

    soup = BeautifulSoup(r.content, 'html.parser')

    product_name = soup.title.get_text()
    product_price = soup.findAll(itemprop="price")[0].get('content')
    product_img_link = soup.find("div", {"id": "product-images-large"}).img.get('content')

    return {
        "product_name": product_name,
        "product_price": product_price,
        "product_img_link": product_img_link
    }

def get_from_amazon(URL):
    r = return_requests(URL)
    # r = requests.get(URL)
    with open("neobyte.html", "wb") as f:
        f.write(r.content)

    soup = BeautifulSoup(r.content, 'html.parser')
    
    product_name = ' '.join([word for word in (soup.findAll(id="productTitle")[0].get_text()).split() if word != " "])
    product_price = soup.findAll("span", {"data-a-color":"price"})[0].get_text()[:6]
    product_img_link = soup.find("div", {"id":"imgTagWrapperId"}).img.get('src')

    return {
        "product_name": product_name,
        "product_price": product_price,
        "product_img_link": product_img_link
    }


def scrape_from_all_links():
    pass

if __name__ == "__main__":
    print(get_from_amazon("https://www.amazon.com/AMD-Ryzen-5950X-32-Thread-Processor/dp/B0815Y8J9N"))