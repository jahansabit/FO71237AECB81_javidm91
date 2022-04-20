import traceback
import time
import json
import datetime
from flask import Flask, request
from pprint import pprint
from bot_vars import *
import subprocess
from difflib import SequenceMatcher

app = Flask('TEST')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def remove_current_url(URL):
    try:
        with open(CURRENT_SCRAPING_FILE_NAMES_DATA_JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    for i in data:
        match_percentage = SequenceMatcher(None, i["url"], URL).ratio() * 100
        if match_percentage > 94:
            data.remove(i)
            break
    with open(CURRENT_SCRAPING_FILE_NAMES_DATA_JSON_FILE_PATH, 'w') as f: 
        json.dump(data, f, indent=4, sort_keys=True)


def find_current_url(URL):
    try:
        with open(CURRENT_SCRAPING_FILE_NAMES_DATA_JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    for i in data:
        match_percentage = SequenceMatcher(None, i["url"], URL).ratio() * 100
        if match_percentage > 94:
            return i["file_name"]
    return None


def write_current_url(URL, file_name):
    try:
        with open(CURRENT_SCRAPING_FILE_NAMES_DATA_JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    data.append({"url": URL, "file_name": file_name})
    with open(CURRENT_SCRAPING_FILE_NAMES_DATA_JSON_FILE_PATH, 'w') as f: 
        json.dump(data, f, indent=4, sort_keys=True)


def read_runtime_urls():
    try:
        with open(RUNTIME_URLS_FILE_PATH, "r") as f:
            RUNTIME_URLS = json.load(f)
    except:
        RUNTIME_URLS = []
    
    return RUNTIME_URLS

def write_runtime_urls(RUNTIME_URLS):
    with open(RUNTIME_URLS_FILE_PATH, "w") as f:
        json.dump(RUNTIME_URLS, f)

@app.route('/', methods=['POST'])
def main():
    # global RUNTIME_URLS
    print(time.strftime('%X %x %Z'))
    main_data = json.loads(request.data)['message']
    print(main_data["title"].lower())

    if "cloudflare" in main_data["title"].lower() or "just a moment" in main_data["title"].lower():
        return "Got Captcha"
    else:
        try:
            RUNTIME_URLS = read_runtime_urls()
            print("RUNTIME_URLS", type(RUNTIME_URLS), RUNTIME_URLS)
            if main_data['url'] not in RUNTIME_URLS:
                RUNTIME_URLS.append(main_data['url'])
                # print(main_data["title"].lower())
                print(main_data["url"])

                file_name = find_current_url(main_data["url"])
                if file_name == None:
                    raise Exception("File name not found") 
                else:
                    remove_current_url(main_data["url"])
                    
                print(file_name)
                print("[*] Writing scrapped html to file...")
                with open(os.path.join(SCRAPPED_DATA_FILES_PATH, file_name), 'w') as f:
                    json.dump(main_data, f)
                print("[*] Finished writing scrapped html to file...")
                with open(SCRAPING_BY_CHROME_DONE_FILE_PATH, 'w') as f:
                    f.write("True")
                # time.sleep(3)
                # shutdown_server()
                write_runtime_urls(RUNTIME_URLS)
                return "Received"
            else:
                print("[*] URL already scrapped")
                return "Already Received"
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return "NOT Received"
    

@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def start_server(URL=None, PORT=FLASK_SERVER_SCRAPER_PORT):
    print("PORT", PORT)
    app.run(host="127.0.0.1", port=PORT)
    # if URL != None:
    #     # subprocess.Popen(str("google-chrome-stable --no-sandbox --log-level=3 " + URL).split(" "))
    #     subprocess.Popen(str("google-chrome-stable --no-sandbox --log-level=3 " + URL).split(" "))
        # time.sleep(2)
    # print("Server started")

# start_server("https://facecom.herokuapp.com/")

if __name__ == "__main__":
    start_server()