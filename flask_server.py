import time
import json
import datetime
from flask import Flask, request
from pprint import pprint
from bot_vars import *

app = Flask('TEST')

@app.route('/', methods=['POST'])
def main():
    print(time.strftime('%X %x %Z'))
    main_data = json.loads(request.data)['message']
    if "cloudflare" in main_data["title"].lower():
        return "Got Captcha"
    elif "pccomponentes.com" in main_data["title"].lower():
        try:
            print(main_data["title"].lower())
            with open(SCRAPPED_DATA_JSON_FILE_PATH, 'w') as f:
                json.dump(main_data, f)
        except Exception as e:
            print(e)
        return "Received"
    else:
        return "Not received"

def start_server():
    app.run(host="127.0.0.1", port=int(5699))
