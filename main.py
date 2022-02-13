#import requests
#import cfscrape
from bs4 import BeautifulSoup
from amazon.page import ama_doc
from neobyte.page import neo_doc
from casemod.page import cas_doc
from pccomponentes.page import pcc_doc


def get_from_pccomponentes():
    soup = BeautifulSoup(pcc_doc, 'html.parser')

    product_name = soup.h1.strong.get_text()
    product_price = soup.findAll(id="precio-main")[0].get("data-price")
    product_img_link = soup.findAll('div',{"class":"item badgets-layer"})[0].a.get("href")

    return {
        "product_name": product_name,
        "product_price": product_price,
        "product_img_link":product_img_link
    }

def get_from_neobyte():
    soup = BeautifulSoup(neo_doc, 'html.parser')

    product_name = soup.title.get_text()
    product_price = soup.findAll(itemprop="price")[0].get('content')
    product_img_link = soup.findAll('div',{"class":"easyzoom easyzoom-product"})[0].a.get("href")

    return {
        "product_name": product_name,
        "product_price": product_price,
        "product_img_link": product_img_link
    }

def get_from_casemod():
    soup = BeautifulSoup(cas_doc, 'html.parser')

    product_name = soup.title.get_text()
    product_price = soup.findAll(itemprop="price")[0].get('content')
    product_img_link = soup.find("div", {"id": "product-images-large"}).img.get('content')

    return {
        "product_name": product_name,
        "product_price": product_price,
        "product_img_link": product_img_link
    }

def get_from_amazon():
    soup = BeautifulSoup(ama_doc, 'html.parser')
    
    product_name = ' '.join([word for word in (soup.findAll(id="productTitle")[0].get_text()).split() if word != " "])
    product_price = soup.findAll("span", {"data-a-color":"price"})[0].get_text()[:6]
    product_img_link = soup.find("div", {"id":"imgTagWrapperId"}).img.get('src')

    return {
        "product_name": product_name,
        "product_price": product_price,
        "product_img_link": product_img_link
    }



if __name__ == "__main__":
    print(get_from_amazon())