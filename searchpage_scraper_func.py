import requests

def return_requests(URL):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'})
    r = s.get(URL, allow_redirects=True)
    cookies = dict(r.cookies)
    # print("cookies -", cookies)
    r = s.post(r.url, allow_redirects=True, verify=False, cookies=cookies)
    return r

def get_from_pccomponentes_searchpage(URL):
    r = return_requests(URL)
    return r.text