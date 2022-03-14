import time
import json
import datetime
from flask import Flask, request
from pprint import pprint
from bot_vars import *

app = Flask('TEST')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/', methods=['POST'])
def main():
    print(time.strftime('%X %x %Z'))
    main_data = json.loads(request.data)['message']
    print(main_data["title"].lower())
    if "cloudflare" in main_data["title"].lower() or "just a moment" in main_data["title"].lower():
        return "Got Captcha"
    else:
        try:
            # print(main_data["title"].lower())
            print("[*] Writing scrapped html to file...")
            with open(SCRAPPED_DATA_JSON_FILE_PATH, 'w') as f:
                json.dump(main_data, f)
            print("[*] Finished writing scrapped html to file...")
        except Exception as e:
            print(e)
        with open(SCRAPING_BY_CHROME_DONE_FILE_PATH, 'w') as f:
            f.write("True")
        return "Received"

@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def start_server():
    app.run(host="127.0.0.1", port=int(5699))
