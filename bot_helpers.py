import json
import string

from bot_vars import *

all=string.maketrans('','')
nodigs=all.translate(all, string.digits)

def load_from_json():
    with open(DATA_JSON_FILE_PATH, 'r') as f:
        data = json.load(f)
        return data

def save_to_json(data):
    with open(DATA_JSON_FILE_PATH, 'a+') as f: 
        json.dump(data, f, indent=4, sort_keys=True)

def add_product_to_file(text):
    try:
        text = text.replace("/add_product", "").strip()
        stripped = text.split(",").strip()
        try:
            link, price = stripped
            price = str(price.translate(all, nodigs))
        except ValueError:
            return "Wrong input format. Example: /add_product https://www.amazon.com/dp/B07JQVZQJF, 10"

        JSON_DATA = load_from_json()
        PRODUCTS_DATA = JSON_DATA["products"]
        NEXT_ID = len(PRODUCTS_DATA) + 1

        PRODUCTS_DATA.append(
            {
                "id": NEXT_ID,
                "link": link,
                "price": price
            }
        )
        JSON_DATA["products"] = PRODUCTS_DATA
            
        save_to_json(JSON_DATA)
        return True
    except Exception as e:
        print(e)
        return str(e)

def delete_product_from_file(text):
    try:
        text = text.replace("/delete_product", "").strip()
        PRODUCT_ID_TO_DELETE = text

        JSON_DATA = load_from_json()
        PRODUCTS_DATA = JSON_DATA["products"]

        product_found = False
        for product in PRODUCTS_DATA:
            if str(product["id"]) == PRODUCT_ID_TO_DELETE:
                PRODUCTS_DATA.remove(product)
                product_found = True
                break
        
        if product_found == False:
            return "Product not found"
        
        JSON_DATA["products"] = PRODUCTS_DATA
        save_to_json(JSON_DATA)
        return True
    except Exception as e:
        print(e)
        return str(e)

def show_products_from_file():
    JSON_DATA = load_from_json()
    PRODUCTS_DATA = JSON_DATA["products"]
    if len(PRODUCTS_DATA) != 0:
        PRODUCTS_DATA = "Products:\n" + "\n".join(map(lambda x: str(x["id"]) + ": " + str(x["link"]) + ", " + str(x["price"]), PRODUCTS_DATA))
    else:
        PRODUCTS_DATA = "No products has been added yet!"
    return PRODUCTS_DATA

def add_channel_to_file(text):
    try:
        text = text.replace("/add_channel", "").strip()
        CHANNEL_NAME = text

        JSON_DATA = load_from_json()
        CHANNELS_DATA = JSON_DATA["channels"]
        NEXT_ID = len(CHANNELS_DATA) + 1

        CHANNELS_DATA.append(
            {
                "id": NEXT_ID,
                "name": CHANNEL_NAME
            }
        )
        JSON_DATA["channels"] = CHANNELS_DATA
            
        save_to_json(JSON_DATA)
        return True
    except Exception as e:
        print(e)
        return str(e)

def remove_channel_from_file(text):
    try:
        text = text.replace("/remove_channel", "").strip()
        CHANNEL_NAME_TO_DELETE = text

        JSON_DATA = load_from_json()
        CHANNELS_DATA = JSON_DATA["channels"]

        channel_found = False
        for channel in CHANNELS_DATA:
            if str(channel["name"]) == CHANNEL_NAME_TO_DELETE:
                CHANNELS_DATA.remove(channel)
                channel_found = True
                break
        
        if channel_found == False:
            return "Channel not found"
        
        JSON_DATA["channels"] = CHANNELS_DATA
        save_to_json(JSON_DATA)
        return True
    except Exception as e:
        print(e)
        return str(e)

def show_channels_from_file():
    JSON_DATA = load_from_json()
    CHANNELS_DATA = JSON_DATA["channels"]
    if len(CHANNELS_DATA) != 0:
        CHANNELS_DATA = "Channels:\n" + "\n".join(map(lambda x: str(x["name"]), CHANNELS_DATA))
    else:
        CHANNELS_DATA = "No channels has been added yet!"
    return CHANNELS_DATA