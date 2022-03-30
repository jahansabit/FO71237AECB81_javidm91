
import traceback
import datetime
from dateutil.parser import *
from scraper_funcs import *
from bot_helpers import *
from bot_vars import *

import os
import json
import telepot
bot = telepot.Bot(BOT_TOKEN)

def check_product_and_send():
    if os.path.isfile(SENT_MSG_DATA_JSON_FILE_PATH) == False:
        main_dict = {}
        main_dict["sent_messages"] = []
        save_sent_msg_to_json(main_dict)

    JSON_DATA = load_from_json()
    CHAT_IDS = JSON_DATA["chat_ids"]
    PRODUCTS = JSON_DATA["products"]
    CHANNELS = JSON_DATA["channels"]
    SENT_MSG_DATA = load_sent_msg_from_json()

    try:
        SHAREABLE_WEBSITES = JSON_DATA["shareable_websites"]
    except:
        SHAREABLE_WEBSITES = []
        SHAREABLE_WEBSITES.append("pccomponentes.com")
        JSON_DATA["shareable_websites"] = SHAREABLE_WEBSITES
        save_to_json(JSON_DATA)

    SCRAPPED_PRODUCTS = []

    browser_tabs = 0

    for i, product in enumerate(PRODUCTS):
        print(product['link'])
        if website_name_provider(product['link']) == "PcComponentes":
            result = get_from_pccomponentes(product['link'])
            browser_tabs += 1
            if browser_tabs >= MAX_BROWSER_TABS:
                browser_tabs = 0
                print("[*] Reached max browser tabs. Closing Chrome...")
                kill_chrome()
                time.sleep(1)
        elif website_name_provider(product['link']) == "Neobyte":
            result = get_from_neobyte(product['link'])
        elif website_name_provider(product['link']) == "Casemod":
            result = get_from_casemod(product['link'])
        elif website_name_provider(product['link']) == "Amazon":
            result = get_from_amazon(product['link'])
        elif website_name_provider(product['link']) == "Coolmod":
            result = get_from_coolmod(product['link'])
        elif website_name_provider(product['link']) == "Aussar":
            result = get_from_aussar(product['link'])
        
        SCRAPPED_PRODUCTS.append(result)
        if result != None:
            # SCRAPPED_PRODUCTS.append(result)
            PRODUCTS[i]["current_price"] = result["product_price"]
            try:
                last_sent_price = PRODUCTS[i]["last_sent_price"]
            except:
                PRODUCTS[i]["last_sent_price"] = "-1"

            try:
                last_availability = PRODUCTS[i]['last_availability']
            except:
                PRODUCTS[i]['last_availability'] = "InStock"

            try:
                availability = PRODUCTS[i]['product_availability']
            except:
                PRODUCTS[i]['product_availability'] = "InStock"

            try:
                last_in_stock = PRODUCTS[i]['last_in_stock']
            except:
                PRODUCTS[i]['last_in_stock'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")   # "1971-1-1 1:1"
        else:
            SCRAPPED_PRODUCTS.append(result)
            print("[*] Product can't be scraped. Skipping...")
            bot.sendMessage(DEBUG_CHAT_ID, "Unable to scrape: " + product['link'])
    
    save_and_send_scrapped_products_report_file(bot, SCRAPPED_PRODUCTS)
    save_and_send_current_products_report_file(bot, PRODUCTS)

    kill_chrome()
    LOG_SENT_MSG_DATA = ""
    for i, scrapped_product in enumerate(SCRAPPED_PRODUCTS):
        if scrapped_product == None:
            continue
        scrapped_product['product_price'] = ''.join(i for i in scrapped_product['product_price'] if (i.isdigit() or i == "."))
        print(scrapped_product['product_price'], PRODUCTS[i]['price'])
        
        try:
            last_availability = PRODUCTS[i]['last_availability']
        except:
            PRODUCTS[i]['last_availability'] = "InStock"
        try:
            availability = scrapped_product['product_availability']
        except:
            scrapped_product['product_availability'] = "InStock"
        
        current_datetime_obj = datetime.datetime.now()
        last_in_stock_datetime_difference = current_datetime_obj - parse(str(PRODUCTS[i]['last_in_stock']))

        LOG_SENT_MSG_DATA += "- Scrapped Product: \n" + str(scrapped_product) + "\n\n"
        LOG_SENT_MSG_DATA += "- Current Product: \n" + str(PRODUCTS[i]) + "\n\n"
        LOG_SENT_MSG_DATA += "- PARENT_LOGIC (float(PRODUCTS[i]['price']) >= float(scrapped_product['product_price'])) : " + str(float(PRODUCTS[i]['price']) >= float(scrapped_product['product_price'])) + "\n\n"
        LOG_SENT_MSG_DATA += "- 1ST_CHILD (float(PRODUCTS[i]['last_sent_price']) != float(scrapped_product['product_price'])) : " + str(float(PRODUCTS[i]['last_sent_price']) != float(scrapped_product['product_price'])) + "\n\n"
        # LOG_SENT_MSG_DATA += "- 2ND_1ST_CHILD (PRODUCTS[i]['last_availability'] != scrapped_product['product_availability']) : " + str(PRODUCTS[i]['last_availability'] != scrapped_product['product_availability']) + "\n\n"
        LOG_SENT_MSG_DATA += "- 2ND_1ST_CHILD (scrapped_product['product_availability'] not in OUT_OF_STOCK_ARRAY) : " + str((scrapped_product['product_availability'] not in OUT_OF_STOCK_ARRAY)) + "\n\n"
        LOG_SENT_MSG_DATA += "- 2ND_2ND_CHILD (last_in_stock_datetime_difference.total_seconds() > z24_HOURS_IN_SECONDS) : " + str(last_in_stock_datetime_difference.total_seconds() > z24_HOURS_IN_SECONDS) + "\n\n"
        LOG_SENT_MSG_DATA += "last_in_stock_datetime_difference: " + str(last_in_stock_datetime_difference) + "\n\n"
        LOG_SENT_MSG_DATA += "======================================================================\n\n"
        # bot.sendMessage(DEBUG_CHAT_ID, LOG_SENT_MSG_DATA, disable_web_page_preview=True, disable_notification=True)

        if float(PRODUCTS[i]['price']) >= float(scrapped_product['product_price']):
            # current_datetime_obj = datetime.datetime.now()
            # last_in_stock_datetime_difference = current_datetime_obj - parse(str(PRODUCTS[i]['last_in_stock']))
            if ((float(PRODUCTS[i]['last_sent_price']) != float(scrapped_product['product_price'])) and (scrapped_product['product_availability'] not in OUT_OF_STOCK_ARRAY)) or\
                ((scrapped_product['product_availability'] not in OUT_OF_STOCK_ARRAY) and (last_in_stock_datetime_difference.total_seconds() > z24_HOURS_IN_SECONDS)):
                print("\n\n")
                print("last_in_stock_datetime_difference", str(last_in_stock_datetime_difference))
                print("\n\n")
                # ((scrapped_product['product_availability'] not in OUT_OF_STOCK_ARRAY) and (last_in_stock_datetime_difference.total_seconds() > z24_HOURS_IN_SECONDS)):
                
                if "https:" not in scrapped_product['product_img_link']:
                    scrapped_product['product_img_link'] = "https:" + scrapped_product['product_img_link']
                try:
                    category = scrapped_product['product_category']
                except:
                    category = ""
                for chat_id in CHAT_IDS:
                    # SEND Customized message to each user, will be customized later
                    bot.sendPhoto(int(chat_id),
                                scrapped_product['product_img_link'],
                                caption=message_template(scrapped_product["product_name"], 
                                    scrapped_product["product_link"],
                                    website_name_provider(scrapped_product['product_link']),
                                    scrapped_product['product_price'], 
                                    PRODUCTS[i]['price'],
                                    category=category), 
                                parse_mode="html")
                    time.sleep(5)
                print(website_name_provider(PRODUCTS[i]['link']) == "PcComponentes")
                # if website_name_provider(PRODUCTS[i]['link']) == "PcComponentes":
                if hostname_provider(PRODUCTS[i]['link']) in SHAREABLE_WEBSITES:
                    for channel in CHANNELS:
                        channel['name'] = channel['name'].replace("https://t.me/", "")
                        channel['name'] = "@" + channel['name'].replace("@", "")
                        # SEND Customized message to each channel, will be customized later
                        print(scrapped_product['product_img_link'], channel['name'])
                        caption = message_template(scrapped_product["product_name"], 
                                                scrapped_product['product_link'],
                                                website_name_provider(scrapped_product['product_link']),
                                                scrapped_product['product_price'], 
                                                PRODUCTS[i]['price'],
                                                category=category)
                        if not DEBUG:
                            result = bot.sendPhoto(channel['name'],
                                                    scrapped_product['product_img_link'],
                                                    caption=caption, 
                                                    parse_mode="html")
                        temp_dict = {}
                        temp_dict["product_from"] = website_name_provider(PRODUCTS[i]['link'])
                        temp_dict["message_data"] = result
                        temp_dict["message_text"] = caption
                        temp_dict["image_link"] = scrapped_product['product_img_link']
                        SENT_MSG_DATA["sent_messages"].append(temp_dict)
                        save_sent_msg_to_json(SENT_MSG_DATA)
                        time.sleep(5)
                PRODUCTS[i]["last_in_stock"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                PRODUCTS[i]["last_sent_price"] = float(scrapped_product['product_price'])
        PRODUCTS[i]["last_availability"] = scrapped_product['product_availability']
            
    save_and_send_string_logs(bot, LOG_SENT_MSG_DATA)
    JSON_DATA["products"] = PRODUCTS
    save_to_json(JSON_DATA)


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
            check_product_and_send()
        except:
            print("\n\n[*] Error occurred. Skipping...\n\n")
            traceback.print_exc()
            bot.sendMessage(DEBUG_CHAT_ID, "Error occurred. \n" + str(traceback.format_exc()))
        print("[*] Product checking is finished... | " + str(time.ctime()))
        # if DEBUG:
        #     break
        os.remove(FLASK_SERVER_RUNNING_FILE_PATH)
        time.sleep(CHECK_FOR_PRODUCTS_EVERY_X_MINUTES * 60)
        # time.sleep(60)
