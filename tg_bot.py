import sys
import os
import time
import json
import telepot
from pprint import pprint

from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import threading

from bot_vars import *
from bot_helpers import *
from scraper import *


if os.path.isfile(DATA_JSON_FILE_PATH) == False:
    main_dict = {}
    main_dict["chat_ids"] = []
    main_dict["chat_ids"].append(USER_CHAT_ID)
    main_dict["products"] = []
    main_dict["channels"] = []
    main_dict["shareable_websites"] = []
    save_to_json(main_dict)
else:
    main_dict = load_from_json()

    # PATCHES
    try:
        temp = main_dict["shareable_websites"]
    except:
        main_dict["shareable_websites"] = []
        main_dict["shareable_websites"].append("pccomponentes.com")
        save_to_json(main_dict)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    try:
        print(content_type, chat_type, chat_id, msg["text"])
    except:
        print(content_type, chat_type, chat_id)
    
    if content_type == 'text':
        if str(chat_id) in main_dict["chat_ids"]:
            if "help" in msg["text"]:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='➕ Add Product', callback_data='add_product')],
                    [InlineKeyboardButton(text='📜 Show Products', callback_data='show_products')],
                    [InlineKeyboardButton(text='🗑️ Delete Products', callback_data='del_product')],
                    [InlineKeyboardButton(text='📺 Channels', callback_data='add_rem_chnl')],
                    [InlineKeyboardButton(text='🌐 Shareable Websites', callback_data='add_rem_webs')],
                    # [InlineKeyboardButton(text='❌ Remove Previous Messages', callback_data='rem_prev_msg')],
                ])

                bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

            elif "/add_channel" in msg["text"]:
                response = add_channel_to_file(msg["text"])
                if response == True:
                    sent = bot.sendMessage(chat_id, "Channel added successfully")
                    pprint(sent)
                else:
                    bot.sendMessage(chat_id, "Error adding channel!\n" + response)

            elif "/remove_channel" in msg["text"]:
                response = remove_channel_from_file(msg["text"])
                if response == True:
                    bot.sendMessage(chat_id, "Channel removed successfully")
                else:
                    bot.sendMessage(chat_id, "Error removing channel!\n" + response)
            
            elif "/show_channels" in msg["text"]:
                response = show_channels_from_file()
                bot.sendMessage(chat_id, response)

            elif "/add_website" in msg["text"]:
                response = add_website_to_file(msg["text"])
                if response == True:
                    bot.sendMessage(chat_id, "Website added successfully")
                else:
                    bot.sendMessage(chat_id, "Error adding website!\n" + response)

            elif "/remove_website" in msg["text"]:
                response = remove_website_from_file(msg["text"])
                if response == True:
                    bot.sendMessage(chat_id, "Website removed successfully")
                else:
                    bot.sendMessage(chat_id, "Error removing website!\n" + response)

            elif "/show_websites" in msg["text"]:
                response = show_websites_from_file()
                bot.sendMessage(chat_id, response)

            elif "/add" in msg["text"]:
                response = add_product_to_file(msg["text"])
                if response == True:
                    bot.sendMessage(chat_id, "Product added successfully")
                else:
                    bot.sendMessage(chat_id, "Error adding product!\n" + response)
            
            elif "/delete" in msg["text"]:
                response = delete_product_from_file(msg["text"])
                if response == True:
                    bot.sendMessage(chat_id, "Product deleted successfully")
                else:
                    bot.sendMessage(chat_id, "Error deleting product!\n" + response)
            
            elif "/show" in msg["text"]:
                response = show_products_from_file()
                for msg in response:
                    bot.sendMessage(chat_id, msg)
                    
            else:
                response = "Sorry, I don't understand you.\n\nUse /help to see the list of commands"
                bot.sendMessage(chat_id, response)
        else:
            links = get_url_from_string(msg["text"])
            print(links)
            for link in links:
                if "pccomponentes.com" in link and "https://www.awin1.com/cread.php?awinmid=20982&awinaffid=870275" not in link:
                    pass

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    # bot.answerCallbackQuery(query_id, text='Got it')
    if str(from_id) in main_dict["chat_ids"]:
        if query_data == "add_product":
            bot.sendMessage(from_id, "To add a product, send me the product name and price like this:\n\n/add product_link, price\n\nExample:\n\n/add https://www.amazon.com/product_name, price")
        elif query_data == "show_products":
            bot.sendMessage(from_id, "Sending you list of products:")
            response = show_products_from_file()
            ## Send Product List
            for msg in response:
                bot.sendMessage(from_id, msg)
        elif query_data == "del_product":
            bot.sendMessage(from_id, "To delete a product, send me the product name like this:\n\n/delete product_id\n\nExample:\n\n/delete 10\n\nTo know the product id, check the product list first: /show")
        elif query_data == "add_rem_chnl":
            bot.sendMessage(from_id, "To add a channel, send me the channel name like this:\n\n/add_channel channel_name")
            bot.sendMessage(from_id, "To remove a channel, send me the channel name like this:\n\n/remove_channel channel_name")
            bot.sendMessage(from_id, "To show channels, send me this command:\n\n/show_channels")
        elif query_data == "add_rem_webs":
            bot.sendMessage(from_id, "To add a website, send me the website name like this:\n\n/add_website https://website.com")
            bot.sendMessage(from_id, "To remove a website, send me the website name like this:\n\n/remove_website https://website.com")
            bot.sendMessage(from_id, "To show websites, send me this command:\n\n/show_websites")
        else:
            response = "Sorry, I don't understand you.\n\nUse /help to see the list of commands"
            bot.sendMessage(from_id, response)

# TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

# Keep scraper thread running.
scraper_thread = threading.Thread(target=periodic_task_thread)
scraper_thread.start()

while 1:
    time.sleep(10)
