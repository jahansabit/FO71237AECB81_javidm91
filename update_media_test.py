import requests
import json

from bot_vars import *

# BOT_TOKEN = ' ... '
CHAT_ID = -1001358908704
MESSAGE_ID = 64

# files = {
#     'media': open('./photo.jpg', 'rb'),
# }
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

print(editMessageMedia(BOT_TOKEN, (CHAT_ID, MESSAGE_ID), TEMP_IMG_LINK))