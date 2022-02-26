
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

    for product in PRODUCTS:
        if website_name_provider(PRODUCTS['link'] == "PcComponentes"):
            result = get_from_pccomponentes(PRODUCTS['link'])
        elif website_name_provider(PRODUCTS['link'] == "Neobyte"):
            result = get_from_neobyte(PRODUCTS['link'])
        elif website_name_provider(PRODUCTS['link'] == "Casemod"):
            result = get_from_casemod(PRODUCTS['link'])
        elif website_name_provider(PRODUCTS['link'] == "Amazon"):
            result = get_from_amazon(PRODUCTS['link'])
        
        SCRAPPED_PRODUCTS.append(result)

    for i, scrapped_product in enumerate(SCRAPPED_PRODUCTS):
        scrapped_product['price'] = ''.join(i for i in scrapped_product['price'] if (i.isdigit() or i == "."))
        if float(scrapped_product['price']) <= float(PRODUCTS[i]['price']):
            for chat_id in CHAT_IDS:
                # SEND Customized message to each user, will be customized later
                bot.sendMessage(channel["name"], "The price of {} has dropped to {}".format(scrapped_product['name'], scrapped_product['price']))
            if website_name_provider(scrapped_product['link'] == "PcComponentes"):
                for channel in CHANNELS:
                    # SEND Customized message to each channel, will be customized later
                    result = bot.sendMessage(channel["name"], "The price of {} has dropped to {}".format(scrapped_product['name'], scrapped_product['price']))
                    temp_dict = {}
                    temp_dict["product_from"] = website_name_provider(scrapped_product['link'])
                    temp_dict["message_data"] = result
                    SENT_MSG_DATA.append(temp_dict)
                    save_sent_msg_to_json(SENT_MSG_DATA)

        
