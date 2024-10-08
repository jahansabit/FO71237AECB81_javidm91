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
from searchpage_scraper_func import *

def kill_chrome():
    try:
        os.system("pkill chrome")
    except:
        print(traceback.format_exc())

def return_requests(URL):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'})
    r = s.get(URL, allow_redirects=True)
    cookies = dict(r.cookies)
    # print("cookies -", cookies)
    r = s.post(r.url, allow_redirects=True, verify=False, cookies=cookies)
    return r

def get_from_pccomponentes(URL): # NOW used only for affiliate link correction
    try:
        os.remove(SCRAPING_BY_CHROME_DONE_FILE_PATH)
    except Exception as e:
        # print(str(e))
        pass

    try:
        soup = return_pccomponentes_page(URL, flask_server_port=FLASK_SERVER_AFFILIATE_PORT)

        try:
            product_name = soup.h1.strong.get_text()
        except:
            product_name = str(soup.find('title').get_text()).replace("| PcComponentes.com", "").strip()
        product_price = soup.findAll(id="precio-main")[0].get("data-price")  # Price here already in international format
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
            print(traceback.format_exc())
            product_category = ""

        try:
            os.remove(SCRAPPED_DATA_JSON_FILE_PATH)
        except Exception as e:
            print(str(e))

        return {
            "product_link": URL,
            "product_name": product_name,
            "product_price": product_price,
            "product_img_link": product_img_link,
            "product_category": product_category,
            "product_availability": availability
        }
    except Exception as e:
        print("\n\nError in get_from_pccomponentes()\n\n")
        print(traceback.format_exc())
        print("\n\n")
        print(str(e))
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
            product_price = soup.findAll(itemprop="price")[0].get('content')  # price already in international format
            product_img_link = soup.findAll('div',{"class":"easyzoom easyzoom-product"})[0].a.get("href")
            availability = str(soup.findAll('link', {"itemprop":"availability"})[0].get("href")).replace("https", "http").replace("http://schema.org/", "")

            return {
                "product_link": URL,
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link,
                "product_availability": availability
            }
        except Exception as e:
            print("\n\nError in get_from_neobyte \n\n")
            print(traceback.format_exc())
            print(str(e))
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
            availability = soup.findAll(itemprop="availability")[0].get('href').replace("https", "http").replace("http://schema.org/", "")
            return {
                "product_link": URL,
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link,
                "product_availability": availability
            }
        except Exception as e:
            print("\n\nError in get_from_casemod \n\n")
            print(traceback.format_exc())
            print(str(e))
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
            # with open("amazon.html", "wb") as f:
            #     f.write(r.content)

            soup = BeautifulSoup(r.content, 'html.parser')
            
            product_name = str(soup.findAll(id="productTitle")[0].get_text()).strip()
            try:
                product_price = str(soup.findAll("span", {"data-a-color":"price"})[0].findAll("span", {"class":"a-offscreen"})[0].get_text()).replace("€", "").strip()
                availability = "InStock"
            except:
                try:
                    ul = soup.findAll("div", {"id":"variation_style_name"})[0].findAll("ul")[0].findAll("li")
                    product_prices = []
                    exception_chars = ["€", ",", ".", " "]
                    price_not_found = True
                    for li in ul:
                        product_price_text = str(li.findAll("div", {"class":"twisterSlotDiv"})[0].get_text())
                        product_price_text = product_price_text.replace(" ", "")  # invisible character
                        price_str = ""
                        if "€" in product_price_text:
                            price_not_found = False
                            # print(product_price_text[::-1])
                            for char in product_price_text[::-1]:
                                # print("char", char)
                                if char not in exception_chars and char.isdigit()==False:
                                    break
                                else:
                                    price_str = char + price_str
                            price_str = price_str.replace("€", "").replace(",", "comma").replace(".", "dot")
                            price_str = price_str.replace("comma", ".").replace("dot", "")
                            product_price = str(float(price_str)) # float for validaiton
                            availability = "InStock"
                        else:
                            pass
                    if price_not_found == True: 
                        raise Exception("Product price not found")
                except:
                    try:
                        price_not_found = True
                        product_prices = soup.findAll("span", {"data-action": "show-all-offers-display"})
                        for item in product_prices:
                            try:
                                product_price = item.findAll("span", {"class": "a-color-price"})[0].get_text().strip()
                                product_price = product_price.replace("€", "").replace(",", "comma").replace(".", "dot")
                                product_price = product_price.replace("comma", ".").replace("dot", "")
                                price_not_found = False
                                availability = "InStock"
                                break
                            except:
                                pass
                        if price_not_found == True: 
                            raise Exception("Product price not found")
                    except Exception as e:
                        # print(traceback.format_exc())
                        print(str(e))
                        product_price = "-1"
                        availability = "OutOfStock"
            product_img_link = soup.find("div", {"id":"imgTagWrapperId"}).img.get('src')

            if product_price != "-1":
                product_price = str(product_price).replace("€", "").replace("€", "").strip()
            
            try:
                product_price = float(product_price)
            except:
                product_price = -1
                availability = "OutOfStock"

            return {
                "product_link": URL,
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link,
                "product_availability": availability
            }
        except Exception as e:
            print("\n\nError in get_from_amazon \n\n")
            print(traceback.format_exc())
            print(str(e))
            time.sleep(3)

def get_from_coolmod(URL):
    print("Scraping:", URL)
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
            
            try:
                product_name = soup.findAll("div", {"class": "productTitle"})[0].get_text()
            except:
                product_name = soup.findAll("h1", {"class": "productTitle"})[0].get_text()
            product_price = str(soup.findAll("span", {"id":"normalpricenumber"})[0].get_text()).replace(",", ".")
            if product_price.count(".") <= 2:
                product_price = product_price.replace(".", "", product_price.count(".") - 1)
            product_img_link = soup.find("img", {"id":"productmainimageitem"}).get('src')
            try:
                breadcumbs = soup.findAll("a", {"class":"coolbreadcrumb"})
                print(len(breadcumbs))
                product_category = breadcumbs[-1].get_text().strip()
            except:
                product_category = "N/A"
            
            # availability = soup.findAll("span", {"id":"messageStock"})[0].get_text() # usable for selenium

            # Avalability Checker
            product_id = str(soup.findAll("div", {"class":"productextrainfotext"})[1].get_text()).strip()
            CatId = soup.find("input", {"id":"subfamily"}).get('value')
            TarId = 1
            DayId = "AM"
            
            spain_timezone = pytz.timezone('Europe/Madrid')
            datetime_obj = datetime.datetime.now(spain_timezone)
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
                "product_category": product_category,
                "product_availability": availability
            }
        except Exception as e:
            print("\n\nError in get_from_coolmod \n\n")
            print(traceback.format_exc())
            print(str(e))
            time.sleep(3)
            print(f"Response Status: {response_status}")
            if (response_status >= 200 and response_status < 300):
                pass
            else:
                return None

def get_from_aussar(URL):
    print("Scraping:", URL)
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
            availability = str(json.loads(soup.findAll("script", {"type":"application/ld+json"})[3].get_text())["offers"]["availability"]).replace("https", "http").replace("http://schema.org/", "")
            try:
                navbar = soup.find("nav", {"class":"breadcrumb"})
                product_category = navbar.findAll("li")[-2].get_text().strip()
            except:
                print(traceback.format_exc())
                product_category = "N/A"
            
            return {
                "product_link": URL,
                "product_name": product_name,
                "product_price": product_price,
                "product_img_link": product_img_link,
                "product_category": product_category,
                "product_availability": availability
            }
        except Exception as e:
            print("\n\nError in get_from_aussar \n\n")
            print(traceback.format_exc())
            print(str(e))
            time.sleep(3)


if __name__ == "__main__":
    # print(get_from_pccomponentes("https://www.pccomponentes.com/gigabyte-radeon-rx-6700-xt-eagle-oc-12gb-gddr6-reacondicionado"))
    # print(get_from_pccomponentes("https://www.pccomponentes.com/asus-tuf-gaming-geforce-gtx-1660-super-oc-edition-6gb-gddr6"))
    # print(get_from_aussar("https://www.aussar.es/tarjetas-graficas/gigabyte-geforce-rtx-3090-gaming-oc-24g.html"))
    # print(get_from_amazon("https://www.amazon.es/Gigabyte-Technology-GV-N306TGAMING-OC-8GD-V2/dp/B09968R87B/ref=sr_1_5?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=33XOP0XZMAP5J&keywords=3060+ti&qid=1649297637&s=amazon-devices&sprefix=3060+ti%2Camazon-devices%2C241&sr=1-5"))
    print(get_from_amazon("https://www.amazon.es/dp/B09TPP2FT9/ref=cm_sw_r_as_gl_api_glt_i_7TQ40PYDZM7TKS8ESCE8?linkCode=ml1&tag=objetivogam0b-21"))
    # print(get_from_coolmod("https://www.coolmod.com/asus-dual-geforce-rtx-3060-ti-oc-lhr-v2-8gb-gddr6-tarjeta-grafica/"))
    pass