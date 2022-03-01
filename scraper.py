
import traceback
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

    SCRAPPED_PRODUCTS = []

    browser_tabs = 0

    for product in PRODUCTS:
        print(product['link'])
        if website_name_provider(product['link']) == "PcComponentes":
            result = get_from_pccomponentes(product['link'])
            browser_tabs += 1
            if browser_tabs > MAX_BROWSER_TABS:
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
        
        if result != None:
            SCRAPPED_PRODUCTS.append(result)
        else:
            print("[*] Product can't be scraped. Skipping...")
            bot.sendMessage(DEBUG_CHAT_ID, "Unable to scrape: " + product['link'])
    
    
    for i, scrapped_product in enumerate(SCRAPPED_PRODUCTS):
        scrapped_product['product_price'] = ''.join(i for i in scrapped_product['product_price'] if (i.isdigit() or i == "."))
        print(scrapped_product['product_price'], PRODUCTS[i]['price'])
        if float(PRODUCTS[i]['price']) >= float(scrapped_product['product_price']):
            if "https:" not in scrapped_product['product_img_link']:
                scrapped_product['product_img_link'] = "https:" + scrapped_product['product_img_link']
            for chat_id in CHAT_IDS:
                # SEND Customized message to each user, will be customized later
                bot.sendPhoto(int(chat_id),
                            scrapped_product['product_img_link'],
                            caption=message_template(scrapped_product["product_name"], 
                                PRODUCTS[i]['link'], 
                                scrapped_product['product_price'], 
                                PRODUCTS[i]['price']), 
                            parse_mode="markdown")
                time.sleep(5)
            print(website_name_provider(PRODUCTS[i]['link']) == "PcComponentes")
            if website_name_provider(PRODUCTS[i]['link']) == "PcComponentes":
                for channel in CHANNELS:
                    # SEND Customized message to each channel, will be customized later
                    print(scrapped_product['product_img_link'], channel['name'])
                    caption = message_template(scrapped_product["product_name"], 
                                            PRODUCTS[i]['link'], 
                                            scrapped_product['product_price'], 
                                            PRODUCTS[i]['price'])
                    result = bot.sendPhoto(channel['name'],
                                            scrapped_product['product_img_link'],
                                            caption=caption, 
                                            parse_mode="markdown")
                    temp_dict = {}
                    temp_dict["product_from"] = website_name_provider(PRODUCTS[i]['link'])
                    temp_dict["message_data"] = result
                    temp_dict["message_text"] = caption
                    temp_dict["image_link"] = scrapped_product['product_img_link']
                    SENT_MSG_DATA["sent_messages"].append(temp_dict)
                    save_sent_msg_to_json(SENT_MSG_DATA)
                    time.sleep(5)
            PRODUCTS[i]['price'] = float(scrapped_product['product_price']) - 0.01
    JSON_DATA["products"] = PRODUCTS
    save_to_json(JSON_DATA)

def periodic_task_thread():
    while True:
        print("[*] Checking for products... | " + str(time.ctime()))
        try:
            check_product_and_send()
        except:
            print("[*] Error occurred. Skipping...")
            bot.sendMessage(DEBUG_CHAT_ID, "Error occurred. \n" + str(traceback.format_exc()))
        print("[*] Product checking is finished... | " + str(time.ctime()))
        time.sleep(CHECK_FOR_PRODUCTS_EVERY_X_MINUTES * 60)
        # time.sleep(60)
