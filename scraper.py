
import traceback
import datetime
import os
import json
import telepot
from dateutil.parser import *
# from urllib3 import Retry
# from scraper_funcs import *
from searchpage_scraper_func import *
from bot_helpers import *
from bot_vars import *
from database import DataBase
# from bot_vars import RUNTIME_URLS_FILE_PATH


bot = telepot.Bot(BOT_TOKEN)
db = DataBase()


def send_product_message_to_channels(scrapped_product, PRODUCT, category):
    # function to prepare channel id and caption
    def prepare_for_sending(channel, scrapped_product, category):
        channel = channel.replace("https://t.me/", "")
        channel = "@" + channel.replace("@", "")
        # SEND Customized message to each channel, will be customized later
        print(scrapped_product['product_img_link'], channel)
        caption = message_template(scrapped_product["product_name"], 
                                scrapped_product['product_link'],
                                website_name_provider(scrapped_product['product_link']),
                                scrapped_product['product_price'], 
                                None,
                                category=category)
        return channel, caption


    for channel in GENERAL_CHANNEL_IDS:
        if hostname_provider(scrapped_product['product_link']) in SHAREABLE_WEBSITES:
            if not DEBUG:
                try:
                    channel, caption = prepare_for_sending(channel, scrapped_product, category)
                    result = bot.sendPhoto(channel,
                                            scrapped_product['product_img_link'],
                                            caption=caption, 
                                            parse_mode="html")
                except:
                    bot.sendMessage(DEBUG_CHAT_ID, "Can't send message to " + str(channel))
                    print(str(traceback.format_exc()))
                time.sleep(3)
            time.sleep(5)
    
    if scrapped_product['channel_id'] != "" or scrapped_product['channel_id'] != None or scrapped_product['channel_id'] != "None":
        if not DEBUG:
            try:
                channel, caption = prepare_for_sending(scrapped_product['channel_id'], scrapped_product, category)
                result = bot.sendPhoto(channel,
                                        scrapped_product['product_img_link'],
                                        caption=caption, 
                                        parse_mode="html")
            except:
                bot.sendMessage(DEBUG_CHAT_ID, "Can't send message to " + str(channel))
                print(str(traceback.format_exc()))
            time.sleep(3)



def check_search_links_and_send():
    JSON_DATA = load_from_json()
    SEARCH_PAGES = db.get_links_json()
    SENT_MSG_DATA = load_sent_msg_from_json()
    RUs = []
    with open(RUNTIME_URLS_FILE_PATH, "w") as f:
        json.dump(RUs, f)

    SCRAPPED_PRODUCTS = []

    browser_tabs = 0

    i = -1
    retry = 0
    while i+1 < len(SEARCH_PAGES):
        #for i, product in enumerate(PRODUCTS):
        i += 1
        page = SEARCH_PAGES[i]
        page_link = page['link']
        price_limit = page['price_limit']
        print(page_link)
        result = None
        try:
            if website_name_provider(page_link) == "PcComponentes":
                result = pccomponentes_page_handler(page_link, price_limit)
                # browser_tabs += 1
                # if browser_tabs >= MAX_BROWSER_TABS:
                #     browser_tabs = 0
                #     print("[*] Reached max browser tabs. Closing Chrome...")
                #     kill_chrome()
                #     time.sleep(1)
            elif website_name_provider(page_link) == "Neobyte":
                result = scrape_neobyte_search_page(page_link)
            elif website_name_provider(page_link) == "Casemod":
                result = scrape_casemod_search_page(page_link)
            elif website_name_provider(page_link) == "Amazon":
                result = scrape_amazon_search_page(page_link)
            elif website_name_provider(page_link) == "Coolmod":
                result = scrape_coolmod_search_page(page_link)
            elif website_name_provider(page_link) == "Aussar":
                result = scrape_aussar_search_page(page_link)
        except:
            traceback.print_exc()
            print("[*] Error in scraping " + page_link)
            continue
        
        if result != None:
            retry = 0
            # UDPATE LAST SCRAPED
            last_scrapped = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))   # "1971-1-1 1:1:1"
            db.update_search_page_last_scraped(i, last_scrapped)
            # Add price limit in every product so that it can be filtered later
            for j, item in enumerate(result):
                print(item['product_name'])
                result[j]['price_limit'] = page['price_limit']
                result[j]['search_page_id'] = page['id']
                result[j]['channel_id'] = page['channel_id']
                result[j]['plus_keywords'] = page['plus_keywords']
                result[j]['minus_keywords'] = page['minus_keywords']
            
            SCRAPPED_PRODUCTS.extend(result)
            print("\n\n[*] Scrapped " + str(len(result)) + " products from " + page_link)
            print("\n")
        else:
            if retry >= 3:
                retry = 0
                print("[*] Retry limit reached. Skipping...")
                bot.sendMessage(DEBUG_CHAT_ID, "[!] Unable to scrape: " + page_link)
                # SCRAPPED_PRODUCTS.extend(result)
            else:
                retry += 1
                i -= 1
                print("[*] Product can't be scraped. Retrying...")
                bot.sendMessage(DEBUG_CHAT_ID, f"[{retry}] Unable to scrape: " + page_link)
        
    
    save_and_send_scrapped_products_report_file(bot, SCRAPPED_PRODUCTS)
    save_and_send_current_products_report_file(bot, SEARCH_PAGES)

    kill_chrome()
    LOG_SENT_MSG_DATA = ""
    for i, scrapped_product in enumerate(SCRAPPED_PRODUCTS):
        if scrapped_product == None:
            continue
        scrapped_product['product_price'] = ''.join(i for i in str(scrapped_product['product_price']) if (i.isdigit() or i == "."))
        print(scrapped_product['product_price'])
        
        
        # current_datetime_obj = datetime.datetime.now()
        # last_in_stock_datetime_difference = current_datetime_obj - parse(str(PRODUCT['last_sent_time']))
        print("\nERROR POINT")
        print(scrapped_product['price_limit'], scrapped_product['product_price'])
        print("ERROR POINT\n")
        if float(scrapped_product['price_limit']) >= float(scrapped_product['product_price']):
            search_result = db.search_product_json(scrapped_product['product_name'], scrapped_product['product_link'])
            
            found_product_in_db = False
            send_product_info = False
            PRODUCT = None
            if len(search_result) > 0:
                print("Product already in DB")
                print(search_result)
                PRODUCT = search_result[0]
                found_product_in_db = True

            if found_product_in_db == False:
                send_product_info = True
            else:
                current_datetime_obj = datetime.datetime.now()
                last_sent_time = PRODUCT['last_sent_time']
                if last_sent_time == None:
                    last_sent_time = "1971-1-1 1:1:1"
                last_in_stock_datetime_difference = current_datetime_obj - parse(str(last_sent_time))
                if ((float(PRODUCT['last_sent_price']) != float(scrapped_product['product_price'])) and (scrapped_product['product_availability'] not in OUT_OF_STOCK_ARRAY)) or\
                    ((scrapped_product['product_availability'] not in OUT_OF_STOCK_ARRAY) and (last_in_stock_datetime_difference.total_seconds() > z24_HOURS_IN_SECONDS)):
                    print("\n\n")
                    print("last_in_stock_datetime_difference", str(last_in_stock_datetime_difference))
                    print("\n\n")
                    # ((scrapped_product['product_availability'] not in OUT_OF_STOCK_ARRAY) and (last_in_stock_datetime_difference.total_seconds() > z24_HOURS_IN_SECONDS)):
                    # send_product_info = True
            
            if send_product_info == True:
                
                try:
                    if (scrapped_product['plus_keywords'] != None and scrapped_product['plus_keywords'] != '' and scrapped_product['plus_keywords'] != 'None'):
                        if scrapped_product['plus_keywords'] not in scrapped_product['product_name']:
                            # send_product_info = False
                            print("\n[+] Will not be sent as plus keywords are not in the", scrapped_product["product_name"])
                            continue
                except KeyError as e:
                    print(str(e))
                    print("[!] KeyError", scrapped_product['product_name'])
                    pass
                
                try:
                    if (scrapped_product['minus_keywords'] != None and scrapped_product['minus_keywords'] != '' and scrapped_product['minus_keywords'] != 'None'):
                        if scrapped_product['minus_keywords'] in scrapped_product['product_name']:
                            # send_product_info = False
                            print("\n[+] Will not be sent as minus keywords are in the", scrapped_product["product_name"])
                            continue
                except KeyError as e:
                    print(str(e))
                    print("[!] KeyError", scrapped_product['product_name'])
                    pass

                if "https:" not in scrapped_product['product_img_link']:
                    scrapped_product['product_img_link'] = "https:" + scrapped_product['product_img_link']
                try:
                    category = scrapped_product['product_category']
                except:
                    category = ""
                for chat_id in CHAT_IDS:
                    # SEND Customized message to each user, will be customized later
                    try:
                        bot.sendPhoto(int(chat_id),
                                    scrapped_product['product_img_link'],
                                    caption=message_template(scrapped_product["product_name"], 
                                        scrapped_product["product_link"],
                                        website_name_provider(scrapped_product['product_link']),
                                        scrapped_product['product_price'], 
                                        None,
                                        category=category), 
                                        parse_mode="html")
                    except:
                        bot.sendMessage(DEBUG_CHAT_ID, "Can't send message to " + str(chat_id))
                        print(str(traceback.format_exc()))
                    time.sleep(5)

                # send product info to channels
                send_product_message_to_channels(scrapped_product, PRODUCT, category)

                # Product is none when it's not found in DB
                scrapped_product['last_sent_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                scrapped_product["last_sent_price"] = float(scrapped_product['product_price'])
                if PRODUCT == None:
                    db.add_product_json(scrapped_product)
                else:
                    scrapped_product['id'] = PRODUCT['id']
                    db.update_product_json(scrapped_product)
                # PRODUCT['last_sent_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # PRODUCT["last_sent_price"] = float(scrapped_product['product_price'])


    # save_and_send_string_logs(bot, LOG_SENT_MSG_DATA)
    # JSON_DATA["products"] = PRODUCTS
    # save_to_json(JSON_DATA)


def periodic_task_thread():
    flask_server_waiting = 0
    while True:
        while os.path.isfile(FLASK_SERVER_RUNNING_FILE_PATH):
            print("FLASK_SERVER_RUNNING_FILE_PATH exists... waiting...")
            time.sleep(3)
            flask_server_waiting += 3
            if flask_server_waiting > FLASK_SERVER_MAX_WAITING_TIME:
                flask_server_waiting = 0
                os.remove(FLASK_SERVER_RUNNING_FILE_PATH)
        
        with open(FLASK_SERVER_RUNNING_FILE_PATH, "w") as f:
            f.write("True")
        print("[*] Checking for products... | " + str(time.ctime()))
        try:
            check_search_links_and_send()
        except:
            print("\n\n[*] Error occurred. Skipping...\n\n")
            traceback.print_exc()
            bot.sendMessage(DEBUG_CHAT_ID, "Error occurred. \n" + str(traceback.format_exc()))
        print("[*] Product checking is finished... | " + str(time.ctime()))
        # if DEBUG:
        #     break
        try:
            os.remove(FLASK_SERVER_RUNNING_FILE_PATH)
        except:
            pass
        time.sleep(CHECK_FOR_PRODUCTS_EVERY_X_MINUTES * 60)
        # time.sleep(60)
