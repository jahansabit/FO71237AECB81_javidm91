
from scraper_funcs import *
from bot_helpers import *
from bot_vars import *

import telepot
bot = telepot.Bot(BOT_TOKEN)

def check_product_and_send():
    JSON_DATA = load_from_json()
    CHAT_IDS = JSON_DATA["chat_ids"]
    PRODUCTS = JSON_DATA["products"]
    CHANNELS = JSON_DATA["channels"]

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
        scrapped_product['price'] = ''.join(i for i in scrapped_product['price'] if i.isdigit())
        if scrapped_product['price'] <= PRODUCTS[i]['price']:
            for chat_id in CHAT_IDS:
                # SEND Customized message to each user, will be customized later
                bot.sendMessage(channel["name"], "The price of {} has dropped to {}".format(scrapped_product['name'], scrapped_product['price']))
            if website_name_provider(scrapped_product['link'] == "PcComponentes"):
                for channel in CHANNELS:
                    # SEND Customized message to each channel, will be customized later
                    bot.sendMessage(channel["name"], "The price of {} has dropped to {}".format(scrapped_product['name'], scrapped_product['price']))


        
