import json
import string
from pprint import pprint
import traceback
import telepot
import time
from urllib.parse import urlparse
import re

from bot_vars import *
from scraper_funcs import *

def get_url_from_string(text):
    # from https://stackoverflow.com/a/28552735
    URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    return re.findall(URL_REGEX, text)


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
    elif link.find("aussar.es") != -1:
        return "Aussar"

def hostname_provider(link):
    parsed_uri = urlparse(link)
    # result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    result = '{uri.netloc}'.format(uri=parsed_uri)
    # print(result)
    if result == '':
        result = link
    return result

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
        text = text.replace("/add", "").strip()
        text = text.replace("  ", " ") # remove double spaces
        stripped = text.split(" ")
        try:
            link, price = stripped
            price = ''.join(i for i in price if (i.isdigit() or i == '.'))
        except ValueError:
            return "Wrong input format. Example: /add https://www.amazon.com/dp/B07JQVZQJF, 10"
        except Exception as e:
            return str(e)

        if price == '' or link == '':
            return "Wrong input format. Example: /add https://www.amazon.com/dp/B07JQVZQJF, 10"

        JSON_DATA = load_from_json()
        PRODUCTS_DATA = JSON_DATA["products"]
        NEXT_ID = len(PRODUCTS_DATA) + 1

        for product in PRODUCTS_DATA:
            if product["link"] in link or link in product["link"]:
                return "Product already in list."

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
        text = text.replace("/delete", "").strip()
        PRODUCT_ID_TO_DELETE = text

        if PRODUCT_ID_TO_DELETE == '':
            return "Wrong input format. Example: /delete 1"

        JSON_DATA = load_from_json()
        PRODUCTS_DATA = JSON_DATA["products"]

        product_found = False
        # for product in PRODUCTS_DATA:
        #     if str(product["id"]) == PRODUCT_ID_TO_DELETE:
        #         PRODUCTS_DATA.remove(product)
        #         product_found = True
        #         break
        
        try:
            PRODUCTS_DATA.pop(int(PRODUCT_ID_TO_DELETE)-1)
            product_found = True
        except:
            print(traceback.format_exc())

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
                PRODUCTS_DATA_STRING += "\n\n" + str(i+1).strip() + " : " + str(PRODUCTS_DATA[i]["link"]).strip() + " , " + str(PRODUCTS_DATA[i]["price"]).strip()
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
            return "Wrong input format. Example: /add_channel @channel_name\nor,   /add_channel https://t.me/channel_name"

        CHANNEL_NAME = CHANNEL_NAME.replace("https://t.me/", "")
        CHANNEL_NAME = "@" + CHANNEL_NAME.replace("@", "")

        JSON_DATA = load_from_json()
        CHANNELS_DATA = JSON_DATA["channels"]
        NEXT_ID = len(CHANNELS_DATA) + 1

        for channel in CHANNELS_DATA:
            if channel["name"] in CHANNEL_NAME or CHANNEL_NAME in channel["name"]:
                return "Channel already in list."

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
            return "Wrong input format. Example: /remove_channel @channel_name\nor,  /remove_channel https://t.me/channel_name"

        CHANNEL_NAME_TO_DELETE = CHANNEL_NAME_TO_DELETE.replace("https://t.me/", "")
        CHANNEL_NAME_TO_DELETE = "@" + CHANNEL_NAME_TO_DELETE.replace("@", "")

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

def add_website_to_file(text):
    try:
        text = text.replace("/add_website", "").strip()
        WEBSITE_NAME = text

        if WEBSITE_NAME == '':
            return "Wrong input format. Example: /add_website https://website.com"

        JSON_DATA = load_from_json()
        WEBSITES_DATA = JSON_DATA["shareable_websites"]
        # NEXT_ID = len(WEBSITES_DATA) + 1

        WEBSITE_NAME = hostname_provider(WEBSITE_NAME)

        for website in WEBSITES_DATA:
            if website in WEBSITE_NAME or WEBSITE_NAME in website:
                return "Website already in list."

        WEBSITES_DATA.append(WEBSITE_NAME)
        JSON_DATA["shareable_websites"] = WEBSITES_DATA
            
        save_to_json(JSON_DATA)
        return True
    except Exception as e:
        traceback.print_exc()
        print(e)
        return str(e)

def remove_website_from_file(text):
    try:
        text = text.replace("/remove_website", "").strip()
        print("text", text)
        WEBSITE_NAME_TO_DELETE = text
        print("WEBSITE_NAME_TO_DELETE", WEBSITE_NAME_TO_DELETE)
        
        if WEBSITE_NAME_TO_DELETE == '':
            return "Wrong input format. Example: /remove_website website.com"

        JSON_DATA = load_from_json()
        WEBSITES_DATA = JSON_DATA["shareable_websites"]

        WEBSITE_NAME_TO_DELETE = hostname_provider(WEBSITE_NAME_TO_DELETE)

        website_found = False
        for website in WEBSITES_DATA:
            print(WEBSITE_NAME_TO_DELETE, website)
            if WEBSITE_NAME_TO_DELETE in website or website in WEBSITE_NAME_TO_DELETE:
                WEBSITES_DATA.remove(website)
                website_found = True
                break
        
        if website_found == False:
            return "Website not found"
        
        JSON_DATA["shareable_websites"] = WEBSITES_DATA
        save_to_json(JSON_DATA)
        return True
    except Exception as e:
        print(e)
        return str(e)

def show_websites_from_file():
    JSON_DATA = load_from_json()
    WEBSITES_DATA = JSON_DATA["shareable_websites"]
    if len(WEBSITES_DATA) != 0:
        WEBSITES_DATA = "Websites:\n" + "\n".join(WEBSITES_DATA)
    else:
        WEBSITES_DATA = "No websites has been added yet!"
    return WEBSITES_DATA

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

def editMessageMedia(BOT_TOKEN, MSG_IDENTIFIER, MEDIA_URL):
    media = json.dumps({
        'type': 'photo',
        'media': MEDIA_URL
    })

    message = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageMedia?chat_id={MSG_IDENTIFIER[0]}&message_id={MSG_IDENTIFIER[1]}&media={media}"

    result = requests.post(message)
    result = result.json()
    try:
        return result['result']
    except Exception as e:
        # print(str(e))
        print(result)
        return result

def remove_and_send_affiliate_link(bot, msg, link):
    try:
        editable_message = bot.sendPhoto(msg['chat']['id'], TEMP_IMG_LINK, caption=PCCOMPONENTES_AFFILIATE_LINK + link, reply_to_message_id=msg['message_id'])
    except Exception as e:
        print(str(e))
        editable_message = bot.sendPhoto(msg['chat']['id'], TEMP_IMG_LINK, caption=PCCOMPONENTES_AFFILIATE_LINK + link)
    
    # editable_message = bot.sendPhoto(msg['chat']['id'], TEMP_IMG_LINK, caption=PCCOMPONENTES_AFFILIATE_LINK + link)
    try:
        bot.deleteMessage(telepot.message_identifier(msg))
    except Exception as e:
        print(str(e))

    scrapped_product = get_from_pccomponentes(link)
    try:
        category = scrapped_product['product_caterory']
    except:
        category = ""

    caption = message_template(scrapped_product["product_name"], 
                                link,
                                website_name_provider(link),
                                scrapped_product['product_price'], 
                                None,
                                category=category)
    editMessageMedia(BOT_TOKEN, telepot.message_identifier(editable_message), scrapped_product['product_img_link'])
    bot.editMessageCaption(telepot.message_identifier(editable_message), caption=caption, parse_mode="html")

# pprint(get_url_from_string("asiufs8dfhse https://www.youtube.com/watch?v=dQw4w9WgXcQ sdvxcfsxscv"))