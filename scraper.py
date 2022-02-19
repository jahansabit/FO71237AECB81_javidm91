
from scraper_funcs import *
from bot_helpers import *
from bot_vars import *

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
    