import sys
import os
import time
import json
import telepot
from pprint import pprint

from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import multiprocessing

from bot_vars import *
from bot_helpers import *
from scraper import *

try:
    os.remove(FLASK_SERVER_RUNNING_FILE_PATH)
except:
    pass

# if os.path.isfile(DATA_JSON_FILE_PATH) == False:
#     main_dict = {}
#     main_dict["chat_ids"] = []
#     main_dict["chat_ids"].append(USER_CHAT_ID)
#     main_dict["products"] = []
#     main_dict["channels"] = []
#     main_dict["shareable_websites"] = []
#     save_to_json(main_dict)
# else:
#     main_dict = load_from_json()

#     # PATCHES
#     try:
#         temp = main_dict["shareable_websites"]
#     except:
#         main_dict["shareable_websites"] = []
#         main_dict["shareable_websites"].append("pccomponentes.com")
#         save_to_json(main_dict)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    msg_id = msg['message_id']
    pprint(msg)
    try:
        print(content_type, chat_type, chat_id, msg["text"])
    except:
        print(content_type, chat_type, chat_id)
    
    if content_type == 'text':
        if str(chat_id) in CHAT_IDS:
            if "help" in msg["text"]:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='➕ Add Search Link', callback_data='add_')],
                    [InlineKeyboardButton(text='📜 Show Search Links', callback_data='show_')],
                    [InlineKeyboardButton(text='🗑️ Delete Search Link', callback_data='del_')],
                    # [InlineKeyboardButton(text='📺 Channels', callback_data='add_rem_chnl')],
                    # [InlineKeyboardButton(text='🌐 Shareable Websites', callback_data='add_rem_webs')],
                    # [InlineKeyboardButton(text='❌ Remove Previous Messages', callback_data='rem_prev_msg')],
                ])

                bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

            elif "/add" in msg["text"]:
                response = add_search_page_link_to_db(msg["text"])
                if response == True:
                    bot.sendMessage(chat_id, "Product added successfully")
                else:
                    bot.sendMessage(chat_id, "Error adding product!\n" + response)
            
            elif "/delete" in msg["text"]:
                response = delete_search_page_link_from_db(msg["text"])
                if response == True:
                    bot.sendMessage(chat_id, "Product deleted successfully")
                else:
                    bot.sendMessage(chat_id, "Error deleting product!\n" + response)
            
            elif "/show" in msg["text"]:
                response = show_search_page_links_from_db()
                for msg in response:
                    bot.sendMessage(chat_id, msg)
                    
            else:
                response = "Sorry, I don't understand you.\n\nUse /help to see the list of commands"
                bot.sendMessage(chat_id, response)
        elif chat_type == "private":
            bot.sendMessage(chat_id, "Sorry. You're not authorized.\n\nYour chat id is: " + str(chat_id))
        # if chats from groups
        else: 
            print("Chat ID not found in main_dict")
            links = get_url_from_string(msg["text"])
            print(links)
            if type(links) == list:
                task = multiprocessing.Process(target=remove_and_send_affiliate_link, args=(bot, msg, links,))
                task.start()
            
            # try:
            #     entities = msg["entities"]
            
            #     for entity in entities:
            #         try:
            #             if entity["url"] not in links:
            #                 if "pccomponentes.com" in entity["url"] and PCCOMPONENTES_AFFILIATE_LINK not in entity["url"]:
            #                     # scrape item details
            #                     # delete user message
            #                     # send item details
            #                     # remove_and_send_affiliate_link(bot, msg, entity["url"])
            #                     threading.Thread(target=remove_and_send_affiliate_link, args=(bot, msg, entity["url"],)).start()
            #                     pass
            #         except Exception as e:
            #             # traceback.print_exc()
            #             print(str(e))
            # except:
            #     traceback.print_exc()

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    # bot.answerCallbackQuery(query_id, text='Got it')
    if str(from_id) in CHAT_IDS:
        if query_data == "add_":
            bot.sendMessage(from_id, "To add a product, send me the product name and price like this:\n\n/add product_link, price\n\nExample:\n\n/add https://www.amazon.com/product_name, price")
        elif query_data == "show_":
            bot.sendMessage(from_id, "Sending you list of products:")
            response = show_search_page_links_from_db()
            ## Send Product List
            for msg in response:
                bot.sendMessage(from_id, msg)
        elif query_data == "del_":
            bot.sendMessage(from_id, "To delete a product, send me the product name like this:\n\n/delete product_id\n\nExample:\n\n/delete 10\n\nTo know the product id, check the product list first: /show")
        else:
            response = "Sorry, I don't understand you.\n\nUse /help to see the list of commands"
            bot.sendMessage(from_id, response)

# TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

print("\n\nBOT STARTED - " + str(time.ctime()))
print("\n\n")
print('Listening ...')

# Keep scraper thread running.
# scraper_thread = threading.Thread(target=periodic_task_thread)
# scraper_thread.start()

bot.sendMessage(DEBUG_CHAT_ID, "Bot started!")
while 1:
    time.sleep(10)
