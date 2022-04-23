import time
from selenium import webdriver
import time, traceback
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib3.exceptions import MaxRetryError
import requests
import os

waiting_standard_seconds = 20

def get_browser(headless=True):
    os.environ["WDM_LOG"] = "0"
    chrome_options = Options()

    try:
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    except:
        pass
    try:
        while(1):
            try:
                time.sleep(1)
                try:
                    s = Service(ChromeDriverManager().install())
                    browser = webdriver.Chrome(service=s, options=chrome_options)
                except:
                    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
                break
            except MaxRetryError:
                print("MaxRetryError! Check your internet connect or try using a vpn!")
                time.sleep(waiting_standard_seconds)
                pass
            except Exception as e:
                print(e)
                time.sleep(10)
    except Exception as e:
        print(e)
        traceback.print_exc()
        browser = None
    return browser

def get_html(URL):
    # if show_browser_window == False:
    #     chrome_options.add_argument('--headless')
    times=3
    x=0
    while x<times:
        waiting_standard_seconds = 20

        times=3
        x=0

        try:
            browser = get_browser(headless=False)
            print(browser)
            ### Main Task
            browser.get(URL)
            
            # print(browser.page_source)
            time.sleep(10)
            # html_body = browser.find_element_by_tag_name("html")
            html_body = WebDriverWait(browser, waiting_standard_seconds).until(EC.visibility_of_element_located((By.TAG_NAME, 'html')))
            html_body = html_body.get_attribute('outerHTML')
            # print(html_body)
            browser.close()
            return html_body
        except MaxRetryError:
            print("MaxRetryError! Check your internet connect or try using a vpn!")
            time.sleep(waiting_standard_seconds)
        except KeyboardInterrupt:
            print("KeyboardInterrupt!")
            browser.close()
            return ""
        except:
            print(str(traceback.format_exc()))

        x+=1

    return None

if __name__ == "__main__":
    # browser = get_browser(headless=False)
    # browser.get("https://cryptorank.io/upcoming-ico")
    # btn = WebDriverWait(browser, waiting_standard_seconds).until(EC.visibility_of_element_located((By.CLASS_NAME, 'styled__ViewAllButton-sc-1hj7kic-4')))
    # btn.click()
    # time.sleep(1)
    # html_body = WebDriverWait(browser, waiting_standard_seconds).until(EC.visibility_of_element_located((By.TAG_NAME, 'html')))
    # html_body = html_body.get_attribute('outerHTML')
    # with open("test.html", "w") as f:
    #     f.write(html_body)
    
    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(html_body, 'html.parser')
    # tag = soup.find_all('div', class_='styled__StyledIcoCard-sc-u5bvc5-1')
    # print(len(tag))
    pass