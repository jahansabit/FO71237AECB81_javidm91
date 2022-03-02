import os
import telepot
from pprint import pprint
from datetime import datetime

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def joinpath(path="", *args):
    return os.path.join(PROJECT_DIR, path, *args)

########## TOKENS ##########
BOT_TOKEN = "5229280387:AAE4SFcTLiDuspR01GydekNgjiLpSSF5qdY"
USER_CHAT_ID = 718057913
DEBUG_CHAT_ID = -744965364
########## TOKENS ##########

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "../tg_bot_data"))
DATA_JSON_FILE_PATH = os.path.join(DATA_DIR, "data.json")
SENT_MSG_DATA_JSON_FILE_PATH = os.path.join(DATA_DIR, "sent_msg_data.json")
SCRAPPED_DATA_JSON_FILE_PATH = os.path.join(DATA_DIR, "scrapped_data.json")
TIME_TO_CHECK_PRODUCTS = 60
CHECK_FOR_PRODUCTS_EVERY_X_MINUTES = 5
MAX_BROWSER_TABS = 5
SCRAPING_MAX_RETRIES = 3
SCRAPPING_MAX_TIMEOUT = 30                  # in seconds
MAX_PRODUCT_IN_SHOW_PRODUCTS_MESSAGE = 7

def message_template(title, link, website_name, current_price, prev_price, category=None):
    current_price = float(current_price)
    prev_price = float(prev_price)
    percentage = prev_price - current_price
    percentage = 100 / prev_price * percentage
    original_link = link
    if "pccomponentes" in link:
        link = "https://www.awin1.com/cread.php?awinmid=20982&awinaffid=870275&ued=" + link
    
    if category == None or category == "":
        category = ""
    else:
        category = "\n<i>#" + category.replace(" ", "_") + "</i>"

    text = f'''
<i>#{website_name}</i>
💥 <b>{title}</b>{category}

🛒 <a href="{link}">COMPRAR AHORA</a>

✅ <b>PRECIO: {str(current_price).replace(".", ",")} €</b>

⭐⭐⭐⭐⭐ 5 de 5

    '''

    return text

# bot = telepot.Bot(BOT_TOKEN)
# result = bot.sendMessage(USER_CHAT_ID, message_template("asdasd", "https://pccomponentes.com", 23, 30), parse_mode="markdown")

# pprint(result)

# print(message_template("title", "https://link", "website_name", "123", "435", category="asasdad"))
# 📉 <b><a href="{link}">Precio MÍNIMO histórico</a></b> ‼️
# <i>Anterior: {str(prev_price).replace(".", ",")} € ({str(datetime.today().strftime('%d-%m-%Y'))})</i>