import sys
import os
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from bot_vars import *

if os.path.isfile(DATA_JSON_FILE_PATH) == False:
    print("Nai")

exit()

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    print(msg["text"])

    if "help" in msg["text"]:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Add Product', callback_data='add_product')],
            [InlineKeyboardButton(text='Show Products', callback_data='show_products')],
            [InlineKeyboardButton(text='Delete Products', callback_data='del_product')],
            [InlineKeyboardButton(text='Add/Remove/Show Channels', callback_data='add_rem_chnl')],
        ])

        bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    # bot.answerCallbackQuery(query_id, text='Got it')

    if query_data == "add_product":
        bot.sendMessage(from_id, "To add a product, send me the product name and price like this:\n\n/add product_link, price\n\nExample:\n\n/add https://www.amazon.com/product_name, price")
    elif query_data == "show_products":
        bot.sendMessage(from_id, "Sending you list of products:")
        ## Send Product List
    elif query_data == "del_product":
        bot.sendMessage(from_id, "To delete a product, send me the product name like this:\n\n/delete product_id\n\nExample:\n\n/delete 10")
    elif query_data == "add_rem_chnl":
        bot.sendMessage(from_id, "To add a channel, send me the channel name like this:\n\n/add_channel channel_name")
        bot.sendMessage(from_id, "To remove a channel, send me the channel name like this:\n\n/remove_channel channel_name")
        bot.sendMessage(from_id, "To show channels, send me this command:\n\n/show_channels")

# TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)