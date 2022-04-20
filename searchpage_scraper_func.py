import requests
from flask_server import *
from bot_vars import *
from scraper_funcs import *
from selenium_functions import *

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
from urllib.parse import urlparse
from urllib.parse import parse_qs

import json

def return_requests(URL):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36', "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"})
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

def return_pccomponentes_page(URL, flask_server_port=FLASK_SERVER_SCRAPER_PORT):
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
            
            server = Process(target=start_server, args=(flask_server_port,))
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
                    r = requests.get(f"http://127.0.0.1:{flask_server_port}/shutdown")
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
                r = requests.get(f"http://127.0.0.1:{flask_server_port}/shutdown")
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

            try:
                os.remove(SCRAPPED_FILE_PATH)
            except Exception as e:
                print(str(e))

            # os.remove(SCRAPPED_DATA_JSON_FILE_PATH)
            html_data = data['html']
            # with open("pcc.html", "w") as f:
            #     f.write(html_data)
            soup = BeautifulSoup(html_data, 'html.parser')

            return soup
        except:
            traceback.print_exc()
            pass

def scrape_pccomponentes_search_page(URL, price_limit):
    # Ordering by price (lower to upper)
    # URL = f"https://www.pccomponentes.com/buscar/?query={query}&price_to={max_price}&or-price_asc"

    parsed_url = urlparse(URL.replace("/query=", "/?query=").replace("#/", ""))
    query = parse_qs(parsed_url.query)['query'][0]
    # if price_limit == None:
    # try:
    #     max_price = parse_qs(parsed_url.query)['price_to'][0]
    # except Exception as e:
    #     traceback.print_exc()
    #     pass

    URL = f"https://www.pccomponentes.com/api-v1/products/search?query={query}&sort=price_asc&channel=es&page=1&pageSize=40&price_to={price_limit}"


    soup = return_pccomponentes_page(URL)
    json_chunk = json.loads(str(soup.findAll('pre')[0].text))['articles']

    all_product_data_json = []

    for item in json_chunk:
        data = {
                "product_link": "N/A",
                "product_name": "N/A",
                "product_price": "N/A",
                "product_img_link": "N/A",
                "product_category": "N/A",
                "product_availability": "N/A"
            }
        data['product_link'] = "https://www.pccomponentes.com/" + item["slug"]
        data['product_name'] = item["name"]
        data['product_price'] = item["originalPrice"]
        try:
            data['product_img_link'] = item["images"]["large"]["path"]
        except:
            try:
                data['product_img_link'] = item["images"]["medium"]["path"]
            except:
                try:
                    data['product_img_link'] = item["images"]["small"]["path"]
                except:
                    data['product_img_link'] = TEMP_IMG_LINK

        data['product_category'] = item["familyName"]
        if str(item['delivery']['availabilityCode']) in ['1', '2', '3']:
            data['product_availability'] = "InStock"
        else:
            data['product_availability'] = "OutOfStock"
       
        all_product_data_json.append(data)
    
    return all_product_data_json

def scrape_pccomponentes_category_page(URL):
    soup = return_pccomponentes_page(URL)
    all_product_data = soup.findAll('article',{"data-price": True})
    all_product_data_json = []

    homepage = "https://www.pccomponentes.com"

    for item in all_product_data:
        data = {
                "product_link": "N/A",
                "product_name": "N/A",
                "product_price": "N/A",
                "product_img_link": "N/A",
                "product_category": "N/A",
                "product_availability": "N/A"
            }
        actual_item = item
        item = item.find('a')
        data['product_link'] = item.get("href")
        if data['product_link'].startswith("/"):
            data['product_link'] = homepage + data['product_link']
        data['product_name'] = item.get("data-name")
        data['product_price'] = item.get("data-price")
        try:
            data['product_img_link'] = actual_item.findAll("img")[0].get("src")
            if data['product_img_link'].startswith("//"):
                data['product_img_link'] = "https:" + data['product_img_link']
            elif data['product_img_link'].startswith("/"):
                data['product_img_link'] = homepage + data['product_img_link']
            data['product_img_link'] = data['product_img_link'].replace("thumb.", "img.").replace("w-220-220/", "")
        except:
            print("can't find pccomponentes product img")
            pass
        data['product_category'] = item.get("data-category")
        data['product_availability'] = item.get("data-stock-web")
        
        if str(data['product_availability']) in ['1', '2', '3']:
            data['product_availability'] = "InStock"
        else:
            data['product_availability'] = "OutOfStock"
        all_product_data_json.append(data)
    
    return all_product_data_json

### TO_BE_DONE
def pccomponentes_page_handler(URL, price_limit):
    if "query" in URL:
        return scrape_pccomponentes_search_page(URL, price_limit)
    else:
        return scrape_pccomponentes_category_page(URL)

def scrape_neobyte_search_page(URL):
    if "order=product.name.asc" not in URL:
        URL = URL + "&order=product.name.asc"
    request_data = return_requests(URL)
    soup = BeautifulSoup(request_data.text, 'html.parser')
    all_product_data = soup.findAll('div',{"class": "js-product-miniature-wrapper"})
    all_product_data_json = []
    # product_category = soup.findAll('nav',{"class": "breadcrumb"})[0].findAll('li')[-1].get_text()

    for item in all_product_data:
        data = {
                "product_link": "N/A",
                "product_name": "N/A",
                "product_price": "N/A",
                "product_img_link": "N/A",
                "product_category": "N/A",
                "product_availability": "N/A"
            }
        data['product_link'] = item.findAll("a", {"class": "product-thumbnail"})[0].get("href")
        try:
            data['product_name'] = item.findAll("span", {"class": "product-title"})[0].get_text().strip()
        except:
            data['product_name'] = item.findAll("h3", {"class": "product-title"})[0].get_text().strip()
        data['product_price'] = item.findAll("span",{"class": "product-price"})[0].get("content").strip()
        data['product_img_link'] = item.findAll("img",{"class": "product-thumbnail-first"})[0].get("data-src")
        data['product_category'] = soup.findAll("div",{"class": "product-category-name"})[0].get_text().strip()
        availability = item.findAll("div",{"class": "product-availability"})[0]
        try:
            availability = availability.findAll("span", {"class":"product-available"})[0]
            data['product_availability'] = "InStock"
        except:
            availability = availability.findAll("span", {"class":"product-unavailable"})[0]
            data['product_availability'] = "OutOfStock"

        all_product_data_json.append(data)
    
    return all_product_data_json

def scrape_casemod_search_page(URL):
    if "order=product.name.asc" not in URL:
        URL = URL + "&order=product.name.asc"
    request_data = return_requests(URL)
    soup = BeautifulSoup(request_data.text, 'html.parser')
    all_product_data = soup.findAll('div',{"class": "js-product-miniature-wrapper"})
    all_product_data_json = []
    # product_category = soup.findAll('nav',{"class": "breadcrumb"})[0].findAll('li')[-1].get_text()

    for item in all_product_data:
        data = {
                "product_link": "N/A",
                "product_name": "N/A",
                "product_price": "N/A",
                "product_img_link": "N/A",
                "product_category": "N/A",
                "product_availability": "N/A"
            }
        data['product_link'] = item.findAll("a", {"class": "product-thumbnail"})[0].get("href")
        try:
            data['product_name'] = item.findAll("span", {"class": "product-title"})[0].get_text().strip()
        except:
            data['product_name'] = item.findAll("h3", {"class": "product-title"})[0].get_text().strip()
        print(data['product_name'])
        data['product_price'] = item.findAll("span",{"class": "product-price"})[0].get("content").strip()
        data['product_img_link'] = item.findAll("img",{"class": "product-thumbnail-first"})[0].get("data-src")
        data['product_category'] = soup.findAll("div",{"class": "product-category-name"})[0].get_text().strip()
        availability = item.findAll("div",{"class": "product-availability"})[0]
        try:
            availability = availability.findAll("span", {"class":"product-available"})[0]
            data['product_availability'] = "InStock"
        except:
            try:
                availability = availability.findAll("span", {"class":"product-unavailable"})[0]
                data['product_availability'] = "OutOfStock"
            except:
                availability = availability.findAll("span", {"class":"product-last-items"})[0]
                data['product_availability'] = "InStock"

        all_product_data_json.append(data)
    
    return all_product_data_json

def scrape_amazon_search_page(URL):
    request_data = return_requests(URL)
    with open("amazon_search_page.html", "w") as f:
        f.write(request_data.text)
    soup = BeautifulSoup(request_data.text, 'html.parser')
    search_results = soup.findAll('div',{"data-asin": True})
    temp_search_results = search_results
    
    for i, search_result in enumerate(temp_search_results):
        if str(search_result.get("data-asin")).strip() == "":
            search_results.pop(i)
    
    all_product_data_json = []

    for item in search_results:
        data = {
                "product_link": "N/A",
                "product_name": "N/A",
                "product_price": "N/A",
                "product_img_link": "N/A",
                "product_category": "N/A",
                "product_availability": "N/A"
            }
        try:
            print("\n")
            data["product_link"] = "https://www.amazon.es/dp/" + item.get("data-asin")
            print(data["product_link"])
            data["product_name"] = item.findAll("span", {"class": "a-size-base-plus a-color-base a-text-normal"})[0].get_text().strip()
            print(data["product_name"])
            try:
                price_str = item.findAll("span", {"class": "a-price-whole"})[0].get_text().strip()
                price_str = price_str.replace("€", "").replace(",", "comma").replace(".", "dot")
                price_str = price_str.replace("comma", ".").replace("dot", "")
                data["product_price"] = price_str
                data["product_availability"] = "InStock" # price scraped, that means it is in stock
            except:
                result = get_from_amazon(data["product_link"])
                data["product_price"] = result["product_price"]
                data["product_availability"] = result["product_availability"]
            
            data["product_img_link"] = item.findAll("img", {"class": "s-image"})[0].get("src")
        except Exception as e:
            print(str(e))
            continue
        
        all_product_data_json.append(data)
        time.sleep(3)
        
    return all_product_data_json


def scrape_coolmod_search_page(URL):
    # url = 'https://www.coolmod.com/#/dffullscreen/query=3060%20ti&filter%5Bg%3Aquantity%5D%5B0%5D=Disponible&session_id=f45cff468c78f960d8571c903497b396&query_name=match_and'
    parsed_url = urlparse(URL.replace("/query=", "/?query=").replace("#/", ""))
    captured_value = parse_qs(parsed_url.query)['query'][0]
    print(parsed_url)
    print(captured_value)

    query = captured_value.replace(" ", "+")

    coolmod_homepage = "https://www.coolmod.com/"

    browser = get_browser(headless=True)
    browser.get(coolmod_homepage)

    search_bar = WebDriverWait(browser, waiting_standard_seconds).until(EC.visibility_of_element_located((By.ID, 'seek')))
    search_bar.click()
    
    time.sleep(1)
    search_bar = WebDriverWait(browser, waiting_standard_seconds).until(EC.visibility_of_element_located((By.ID, 'df-searchbox__dffullscreen')))
    search_bar.send_keys(query)
    time.sleep(4)
    
    search_instock_only = True

    try:
        browser.find_element(by=By.XPATH, value='//div[@data-value="Disponible"]').click() # InStock Filter
        time.sleep(4)
    except:
        search_instock_only = False
        print("Disponible", "Item not found")
    
    search_results = browser.find_elements(by=By.CLASS_NAME, value='df-card')
    all_product_data_json = []

    for i, item in enumerate(search_results):
        data = {
                "product_link": "N/A",
                "product_name": "N/A",
                "product_price": "N/A",
                "product_img_link": "N/A",
                "product_category": "N/A",
                "product_availability": "N/A"
            }
        
        data["product_link"] = item.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        data["product_name"] = item.find_element(by=By.CLASS_NAME, value='df-card__title').text.strip()
        price_str = item.find_element(by=By.CLASS_NAME, value='df-card__price').text.strip()
        price_str = price_str.replace("€", "").replace(",", "comma").replace(".", "dot")
        price_str = price_str.replace("comma", ".").replace("dot", "")
        data["product_price"] = price_str
        data["product_img_link"] = item.find_element(by=By.TAG_NAME, value='img').get_attribute('src')
        
        product = get_from_coolmod(data["product_link"])
        if search_instock_only == True:
            data["product_availability"] = "InStock"
        else:
            pass

        if product != None:
            data["product_availability"] = product["product_availability"]
            data["product_category"] = product["product_category"]
            data["product_img_link"] = product["product_img_link"]

        all_product_data_json.append(data)
        time.sleep(3)

    browser.close()
    return all_product_data_json

def scrape_aussar_search_page(URL):
    # url = 'https://www.aussar.es/#/dfclassic/query=dfg&session_id=7f5a58bd3b4a510b1fb708a043027f4d&query_name=fuzzy'
    parsed_url = urlparse(URL.replace("/query=", "/?query=").replace("#/", ""))
    print(parsed_url)
    captured_value = parse_qs(parsed_url.query)['query'][0]
    print(captured_value)

    query = captured_value.replace(" ", "+")

    coolmod_homepage = "https://www.aussar.es/"

    browser = get_browser(headless=True)
    browser.get(coolmod_homepage)

    search_bar = WebDriverWait(browser, waiting_standard_seconds).until(EC.visibility_of_element_located((By.ID, 'leo_search_query_top')))
    search_bar.click()
    time.sleep(1)
    search_bar.send_keys(query)
    time.sleep(4)
    
    search_instock_only = True

    try:
        browser.find_element(by=By.XPATH, value='//div[@data-value="in stock"]').click()
        time.sleep(4)
    except:
        search_instock_only = False
        print("Disponible", "Item not found")
    
    search_results = browser.find_elements(by=By.CLASS_NAME, value='df-card')
    all_product_data_json = []

    for i, item in enumerate(search_results):
        data = {
                "product_link": "N/A",
                "product_name": "N/A",
                "product_price": "N/A",
                "product_img_link": "N/A",
                "product_category": "N/A",
                "product_availability": "N/A"
            }
        
        data["product_link"] = item.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        data["product_name"] = item.find_element(by=By.CLASS_NAME, value='df-card__title').text.strip()
        price_str = item.find_element(by=By.CLASS_NAME, value='df-card__pricing').text.strip()
        price_str = price_str.replace("€", "").replace(",", "comma").replace(".", "dot")
        price_str = price_str.replace("comma", ".").replace("dot", "")
        data["product_price"] = price_str
        data["product_img_link"] = item.find_element(by=By.TAG_NAME, value='img').get_attribute('src')
        
        product = get_from_aussar(data["product_link"])
        if search_instock_only == True:
            data["product_availability"] = "InStock"
        else:
            pass

        if product != None:
            data["product_availability"] = product["product_availability"]
            data["product_category"] = product["product_category"]
            data["product_img_link"] = product["product_img_link"]

        all_product_data_json.append(data)
        time.sleep(3)

    browser.close()
    return all_product_data_json

if __name__ == "__main__":
    RUs = []
    with open(RUNTIME_URLS_FILE_PATH, "w") as f:
        json.dump(RUs, f)
    # print(scrape_pccomponentes_search_page("rtx 3060", 400))
    # print(scrape_neobyte_search_page("https://www.neobyte.es/tarjetas-graficas-111"))
    # print(scrape_neobyte_search_page("https://www.neobyte.es/buscador?s=3060+ti"))
    # print(scrape_casemod_search_page("https://casemod.es/jolisearch?s=3060+ti"))
    # print(scrape_amazon_search_page("https://www.amazon.es/s?k=3060+ti"))
    # print(scrape_coolmod_search_page("https://www.coolmod.com/#/dffullscreen/query=3060%20ti&filter%5Bg%3Aquantity%5D%5B0%5D=Disponible&session_id=f45cff468c78f960d8571c903497b396&query_name=match_and"))
    # print(scrape_aussar_search_page("https://www.aussar.es/tarjetas-graficas/gigabyte-geforce-rtx-3090-gaming-oc-24g.html#/dfclassic/query=3060%20ti&session_id=7f5a58bd3b4a510b1fb708a043027f4d&query_name=match_and")) 
    # print(pccomponentes_page_handler("https://pccomponentes.com/tarjetas-graficas", 500))
    # print(pccomponentes_page_handler("https://www.pccomponentes.com/buscar/?query=rtx%203080%20ti&price_to=400&or-price_asc", 500))