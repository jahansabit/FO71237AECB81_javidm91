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
from database import DataBase
db = DataBase()

def debug_print(msg):
    if DEBUG:
        print(msg)

def get_url_from_string(text):
    # from https://stackoverflow.com/a/28552735
    URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    return re.findall(URL_REGEX, text)


def website_name_provider(link):
    if link.find("amazon.es") != -1 or link.find("amazon.com") != -1:
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
    else:
        return "Unknown"

def hostname_provider(link):
    parsed_uri = urlparse(link)
    # result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    result = '{uri.netloc}'.format(uri=parsed_uri)
    # print(result)
    if result == '':
        result = link
    return result

def load_from_json():
    with open(DATA_SEARCH_PAGE_JSON_FILE_PATH, 'r') as f:
        data = json.load(f)
    return data

def save_to_json(data):
    with open(DATA_SEARCH_PAGE_JSON_FILE_PATH, 'w') as f: 
        json.dump(data, f, indent=4, sort_keys=True)

def load_sent_msg_from_json():
    with open(DATA_SEARCH_PAGE_JSON_FILE_PATH, 'r') as f:
        data = json.load(f)
    return data

def save_sent_msg_to_json(data):
    with open(DATA_SEARCH_PAGE_JSON_FILE_PATH, 'w') as f: 
        json.dump(data, f, indent=4, sort_keys=True)

def save_and_send_scrapped_products_report_file(bot, products_data):
    with open(SCRAPPED_PRODUCTS_REPORT_FILE_PATH, 'w') as f: 
        json.dump(products_data, f, indent=4, sort_keys=True)
    bot.sendDocument(DEBUG_CHAT_ID, open(SCRAPPED_PRODUCTS_REPORT_FILE_PATH, 'rb'), caption="Scrapped Products Report", disable_notification=True)

def save_and_send_current_products_report_file(bot, products_data):
    with open(CURRENT_PRODUCTS_REPORT_FILE_PATH, 'w') as f: 
        json.dump(products_data, f, indent=4, sort_keys=True)
    bot.sendDocument(DEBUG_CHAT_ID, open(CURRENT_PRODUCTS_REPORT_FILE_PATH, 'rb'), caption="Current Products Report", disable_notification=True)

def save_and_send_string_logs(bot, text):
    with open(LOGS_FILE_PATH, 'w') as f: 
        f.write(text + "\n")
    bot.sendDocument(DEBUG_CHAT_ID, open(LOGS_FILE_PATH, 'rb'), caption="Text Logs", disable_notification=True)

def check_if_number(string):
    try:
        num = float(string)
        return True
    except:
        return False

def add_search_page_link_to_db(msg_text):
    # /add link price +keywords -keywords channel
    try:
        msg_text = msg_text.replace("/add", "").strip() # /add link price channel
        msg_text = msg_text.replace("  ", " ") # remove double spaces
        splitted = msg_text.split(" ") # link price +keywords -keywords channel
        link = None
        price = None
        plus_keywords = None
        minus_keywords = None
        channel = None
        for phrase in splitted:
            if "http" in phrase or "https" in phrase:
                link = phrase
            elif check_if_number(phrase)==True and '-' not in phrase:
                price = phrase.strip()
                price = ''.join(i for i in price if (i.isdigit() or i == ','))
                price = str(price).replace(",", ".")
            elif '+' in phrase:
                plus_keywords = phrase.replace("+", " ")
            elif phrase == splitted[len(splitted)-1] and '+' not in phrase and (phrase.startswith('@') or phrase.startswith('-')):
                channel = phrase.strip()
            elif '-' in phrase:
                minus_keywords = phrase.replace("-", " ") # there is a reason why it is at the end. private channels can have '-' in their name
        if link == None or price == None:
            return "Wrong input format. Example: /add https://www.amazon.es/***/**** 10\n/add https://www.amazon.es/***/**** 10 rtx+3060 ti- channel_id"

        if price == '' or link == '':
            return "Wrong input format. Example: /add https://www.amazon.es/***/**** 10\n/add https://www.amazon.es/***/**** 10 rtx+3060 ti- channel_id"

        all_search_pages = db.get_links_json()
        all_search_pages_links = [search_page['link'] for search_page in all_search_pages]


        for search_page_link in all_search_pages_links:
            if search_page_link in link or link in search_page_link:
                return "Product already in list."

        db.add_link(link, price, plus_keywords, minus_keywords, channel)
        return True
    except Exception as e:
        print(e)
        return str(e)

def delete_search_page_link_from_db(msg_text):
    try:
        msg_text = msg_text.replace("/delete", "").strip()
        SEARCH_PAGE_ID_TO_DELETE = msg_text

        if SEARCH_PAGE_ID_TO_DELETE == '':
            return "Wrong input format. Example: /delete 1"

        product_found = False
        
        try:
            db.delete_link(int(SEARCH_PAGE_ID_TO_DELETE)-1)
            product_found = True
        except:
            print(traceback.format_exc())

        if product_found == False:
            return "Product not found"
        
        return True
    except Exception as e:
        print(e)
        return str(e)

def show_search_page_links_from_db():
    SEARCH_PAGES_DATA = db.get_links_json()
    result_array = []
    if len(SEARCH_PAGES_DATA) != 0:
        # SEARCH_PAGES_DATA = "Products:\n" + "\n".join(map(lambda x: str(x["id"]) + ": " + str(x["link"]) + ", " + str(x["price"]), SEARCH_PAGES_DATA))
        
        SEARCH_PAGES_DATA_STRING = "Products:\nID\tLink\tPrice\tChannel\n"

        for i, entry in enumerate(SEARCH_PAGES_DATA):
            temp = "\n\n" + str(i+1).strip() + " : " + str(entry['link']).strip() + " , " + str(entry['price_limit']).strip() + " , " + str(entry['channel_id']).strip()
            if i == 0:
                SEARCH_PAGES_DATA_STRING += temp
            else:
                SEARCH_PAGES_DATA_STRING = temp
            result_array.append(SEARCH_PAGES_DATA_STRING)
        # print(len(result_array))
        return result_array   
    else:
        SEARCH_PAGES_DATA = ["No Search_Page_links has been added yet!"]
        return SEARCH_PAGES_DATA

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

def process_removing_affiliate_link(bot, msg, link, actual_link): # link with affiliate id and tags
    try:
        reply_to_msg_id = int(msg['message_id'])
        editable_message = bot.sendPhoto(int(msg['chat']['id']), TEMP_IMG_LINK, caption=link, reply_to_message_id=reply_to_msg_id)
    except Exception as e:
        traceback.print_exc()
        time.sleep(1)
        # editable_message = bot.sendPhoto(int(msg['chat']['id']), TEMP_IMG_LINK, caption=link)
    
    time.sleep(1)
    try:
        bot.deleteMessage(telepot.message_identifier(msg))
    except Exception as e:
        print(str(e))
    time.sleep(1)
    
    if website_name_provider(actual_link) == "PcComponentes":
        scrapped_product = get_from_pccomponentes(actual_link)
    elif website_name_provider(actual_link) == "Amazon":
        scrapped_product = get_from_amazon(actual_link)

    try:
        category = scrapped_product['product_category']
    except:
        category = ""
    
    while(type(scrapped_product) != dict):
        time.sleep(1)

    print(scrapped_product)
    print("\n")

    print(scrapped_product["product_name"], 
                                link,
                                website_name_provider(link),
                                scrapped_product['product_price'], 
                                None,
                                category)

    caption = message_template(scrapped_product["product_name"], 
                                link,
                                website_name_provider(link),
                                scrapped_product['product_price'], 
                                None,
                                category=category)
    editMessageMedia(BOT_TOKEN, telepot.message_identifier(editable_message), scrapped_product['product_img_link'])
    time.sleep(1)
    bot.editMessageCaption(telepot.message_identifier(editable_message), caption=caption, parse_mode="html")
    time.sleep(1)

def read_affiliate_links_json_from_file():
    try:
        with open(SEND_AFFILIATE_URLS_FILE_PATH, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(e)
        return []

def write_affiliate_links_json_to_file(data):
    try:
        with open(SEND_AFFILIATE_URLS_FILE_PATH, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(e)

def remove_and_send_affiliate_link(bot, msg, links):

    # flask_server_waiting = 0
    # while os.path.isfile(FLASK_SERVER_RUNNING_FILE_PATH):
    #     print("FLASK_SERVER_RUNNING_FILE_PATH exists... waiting...")
    #     time.sleep(3)
    #     flask_server_waiting += 3
    #     if flask_server_waiting > FLASK_SERVER_MAX_WAITING_TIME:
    #         flask_server_waiting = 0
    #         os.remove(FLASK_SERVER_RUNNING_FILE_PATH)
    
    # with open(FLASK_SERVER_RUNNING_FILE_PATH, "w") as f:
    #     f.write("True")
    if type(links) == list:
        for link in links:
            prev_affiliate_links = read_affiliate_links_json_from_file()
            if any(link in s['link'] and s['message_id']==msg['message_id'] and s['chat_id']==msg['chat']['id']  for s in prev_affiliate_links):
                print("Link already exists in the file")
                continue
            prev_affiliate_links.append({"link": link, "message_id": msg['message_id'], "chat_id": msg['chat']['id']})
            write_affiliate_links_json_to_file(prev_affiliate_links)

            if "pccomponentes.com" in link and PCCOMPONENTES_AFFILIATE_LINK not in link:
                process_removing_affiliate_link(bot, msg, PCCOMPONENTES_AFFILIATE_LINK+link, link)
            elif "amazon.es" in link and AMAZON_AFFILIATE_LINK not in link:
                link_arr = link.split("/")
                if "linkCode" in link_arr[-1] or "tag=" in link_arr[-1]:
                    link_arr.pop()
                link = "/".join(link_arr)
                process_removing_affiliate_link(bot, msg, link+AMAZON_AFFILIATE_LINK, link)

    try:
        os.remove(FLASK_SERVER_RUNNING_FILE_PATH)
    except:
        pass

if __name__ == "__main__":
    # print(show_search_page_links_from_db())
    print(hostname_provider("https://pccomponentes.com/buscar/?query=rtx%203080%20ti&price_to=400&or-price_asc"))