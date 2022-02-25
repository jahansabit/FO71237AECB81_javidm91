import time
import json
import datetime
from flask import Flask, request
from scraper_funcs import get_from_pccomponentes
from pprint import pprint

app = Flask('TEST')

@app.route('/', methods=['POST'])
def main():
    print(time.strftime('%X %x %Z'))
    main_data = json.loads(request.data)['message']
    if "cloudflare" in main_data["title"].lower():
        pass
    else:
        response = get_from_pccomponentes("", main_data["html"])
        pprint(response)
    
    return "Received"

app.run(host="127.0.0.1", port=int(5699))
