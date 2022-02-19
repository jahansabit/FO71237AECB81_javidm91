import sys
import os
import time
import json
import telepot
from pprint import pprint

from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from bot_vars import *
from bot_helpers import *


if os.path.isfile(DATA_JSON_FILE_PATH) == False:
    main_dict = {}
    main_dict["chat_ids"] = []
    main_dict["chat_ids"].append(USER_CHAT_ID)
    main_dict["products"] = []
    main_dict["channels"] = []
    save_to_json(main_dict)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg["text"])

    if "help" in msg["text"]:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Add Product', callback_data='add_product')],
            [InlineKeyboardButton(text='Show Products', callback_data='show_products')],
            [InlineKeyboardButton(text='Delete Products', callback_data='del_product')],
            [InlineKeyboardButton(text='Add/Remove/Show Channels', callback_data='add_rem_chnl')],
            [InlineKeyboardButton(text='Remove Previous Messages', callback_data='rem_prev_msg')],
        ])

        bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)
    
    elif "/add_product" in msg["text"]:
        response = add_product_to_file(msg["text"])
        if response == True:
            bot.sendMessage(chat_id, "Product added successfully")
        else:
            bot.sendMessage(chat_id, "Error adding product!\n" + response)
    
    elif "/delete_product" in msg["text"]:
        response = delete_product_from_file(msg["text"])
        if response == True:
            bot.sendMessage(chat_id, "Product deleted successfully")
        else:
            bot.sendMessage(chat_id, "Error deleting product!\n" + response)
    
    elif "/show_products" in msg["text"]:
        response = show_products_from_file()
        bot.sendMessage(chat_id, response)

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
    # else:
    #     msg = "Sorry, I don't understand you.\n\nUse /help to see the list of commands"
    #     telepot.message_identifier(msg)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    # bot.answerCallbackQuery(query_id, text='Got it')

    if query_data == "add_product":
        bot.sendMessage(from_id, "To add a product, send me the product name and price like this:\n\n/add_product product_link, price\n\nExample:\n\n/add_product https://www.amazon.com/product_name, price")
    elif query_data == "show_products":
        bot.sendMessage(from_id, "Sending you list of products:")
        ## Send Product List
    elif query_data == "del_product":
        bot.sendMessage(from_id, "To delete a product, send me the product name like this:\n\n/delete_product product_id\n\nExample:\n\n/delete_product 10\n\nTo know the product id, check the product list first: /show_products")
    elif query_data == "add_rem_chnl":
        bot.sendMessage(from_id, "To add a channel, send me the channel name like this:\n\n/add_channel channel_name")
        bot.sendMessage(from_id, "To remove a channel, send me the channel name like this:\n\n/remove_channel channel_name")
        bot.sendMessage(from_id, "To show channels, send me this command:\n\n/show_channels")
    elif query_data == "rem_prev_msg":
        bot.sendMessage(from_id, "Removing previous messages.\nPlease wait...")

# TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')
# data = {
#     "chat": {
#         "id": 718057913,
#     },
#     "message_id": 16567
# }
# pprint(telepot.message_identifier(data))

while 1:
    time.sleep(10)