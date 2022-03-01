import json
import string
from pprint import pprint
import telepot
import time

from bot_vars import *

def website_name_provider(link):
    if link.find("amazon.com") != -1:
        return "Amazon"
    elif link.find("pccomponentes.com") != -1:
        return "PcComponentes"
    elif link.find("neobyte.es") != -1:
        return "Neobyte"
    elif link.find("casemod.es") != -1:
        return "Casemod"
    elif link.find("coolmod.com") != -1:
        return "Coolmod"

def load_from_json():
    with open(DATA_JSON_FILE_PATH, 'r') as f:
        data = json.load(f)
        return data

def save_to_json(data):
    with open(DATA_JSON_FILE_PATH, 'w') as f: 
        json.dump(data, f, indent=4, sort_keys=True)

def load_sent_msg_from_json():
    with open(SENT_MSG_DATA_JSON_FILE_PATH, 'r') as f:
        data = json.load(f)
        return data

def save_sent_msg_to_json(data):
    with open(SENT_MSG_DATA_JSON_FILE_PATH, 'w') as f: 
        json.dump(data, f, indent=4, sort_keys=True)

def add_product_to_file(text):
    try:
        text = text.replace("/add_product", "").strip()
        stripped = text.split(",")
        try:
            link, price = stripped
            price = ''.join(i for i in price if (i.isdigit() or i == '.'))
        except ValueError:
            return "Wrong input format. Example: /add_product https://www.amazon.com/dp/B07JQVZQJF, 10"
        except Exception as e:
            return str(e)

        if price == '' or link == '':
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

        if PRODUCT_ID_TO_DELETE == '':
            return "Wrong input format. Example: /delete_product 1"

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
    result_array = []
    if len(PRODUCTS_DATA) != 0:
        # PRODUCTS_DATA = "Products:\n" + "\n".join(map(lambda x: str(x["id"]) + ": " + str(x["link"]) + ", " + str(x["price"]), PRODUCTS_DATA))
        i = 0
        upper_limit = 0
        while 1:
            PRODUCTS_DATA_STRING = ""
            i = upper_limit
            upper_limit = i + MAX_PRODUCT_IN_SHOW_PRODUCTS_MESSAGE
            if upper_limit > len(PRODUCTS_DATA):
                upper_limit = len(PRODUCTS_DATA)
            # print(i, upper_limit, len(PRODUCTS_DATA))

            if i == 0:
                PRODUCTS_DATA_STRING += "Products:\nID\tLink\tPrice\n"

            for i in range(i, upper_limit):
                # print(str(PRODUCTS_DATA[i]["id"]).strip() + " : " + str(PRODUCTS_DATA[i]["link"]).strip() + " , " + str(PRODUCTS_DATA[i]["price"]).strip())
                PRODUCTS_DATA_STRING += "\n\n" + str(PRODUCTS_DATA[i]["id"]).strip() + " : " + str(PRODUCTS_DATA[i]["link"]).strip() + " , " + str(PRODUCTS_DATA[i]["price"]).strip()
            result_array.append(PRODUCTS_DATA_STRING)
            if upper_limit == len(PRODUCTS_DATA):
                break
        # print(len(result_array))
        return result_array   
    else:
        PRODUCTS_DATA = ["No products has been added yet!"]
        return PRODUCTS_DATA

def add_channel_to_file(text):
    try:
        text = text.replace("/add_channel", "").strip()
        CHANNEL_NAME = text

        if CHANNEL_NAME == '':
            return "Wrong input format. Example: /add_channel @channel_name"

        CHANNEL_NAME = CHANNEL_NAME.replace("https://t.me/", "")
        CHANNEL_NAME = "@" + CHANNEL_NAME.replace("@", "")

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
        
        if CHANNEL_NAME_TO_DELETE == '':
            return "Wrong input format. Example: /remove_channel @channel_name"

        JSON_DATA = load_from_json()
        CHANNELS_DATA = JSON_DATA["channels"]

        channel_found = False
        for channel in CHANNELS_DATA:
            if str(channel["name"]) == CHANNEL_NAME_TO_DELETE or str(channel["name"]) in CHANNEL_NAME_TO_DELETE:
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

def delete_pccomponentes_messages(bot):
    sent_messages = load_sent_msg_from_json()
    for message in sent_messages["sent_messages"]:
        if message["product_from"] == "PcComponentes":
            msg_identifier = telepot.message_identifier(message["message_data"])
            try:
                bot.deleteMessage(msg_identifier)
            except Exception as e:
                print(e)
                print("msg_identifier:", msg_identifier)
            time.sleep(1)
            bot.sendPhoto(message["message_data"]['chat']['id'],
                        message['image_link'],
                        caption=message['message_text'], 
                        parse_mode="markdown")
        time.sleep(5)
            
pprint(len(show_products_from_file()))