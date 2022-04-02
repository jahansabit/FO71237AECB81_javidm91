import requests
from pprint import pprint
import json

# url = "https://www.pccomponentes.com/api-v1/products/search?query=3060%20ti&channel=es&page=17&pageSize=40"
# cookies = "_ALGOLIA=anonymous-736dd7ed-5a68-4aba-aa96-dcf2263bd277; _gcl_au=1.1.629635145.1646394939; _ga_B8JPB9S1S2=GS1.1.1647408341.2.0.1647410006.0; _ga=GA1.2.1878279108.1646394940; _aw_m_20982=20982_1647408320_2cd55359b8bfc33072b3340db5a33e80; _uetvid=037bdce09bb211ec9eb91f1fb38bbf83; _fbp=fb.1.1647408343710.817457375; _hjSessionUser_272199=eyJpZCI6Ijk0YzZjNmQ0LWFjZGYtNWZiNS1iMzA2LTY3NjhmNzc4MGU1MSIsImNyZWF0ZWQiOjE2NDc0MDgzNDQxMjEsImV4aXN0aW5nIjpmYWxzZX0=; __gads=ID=66a3cf6eada65a3d-22d6811702d10068:T=1647408343:S=ALNI_Ma-cQVmDMYLZyZSeYonCVSJat7txA; _clck=fwmvhx|1|ezt|0; adformfrpid=178425879135349874; acept_cookie=1; AMCVS_860375D55F463E4C0A495FE8%40AdobeOrg=1; cf_chl_2=e9bb64e856041ec; cf_chl_prog=x13; mbox=PC#ae092b8111e541e580df7fa7cd12f3e7.38_0#1710653142|session#2187d96212504285ad55bc202bf6f873#1648857036; AMCV_860375D55F463E4C0A495FE8%40AdobeOrg=-1124106680%7CMCIDTS%7C19084%7CMCMID%7C41964973734111531132683837136203810391%7CMCAAMLH-1648013139%7C3%7CMCAAMB-1648815957%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1648862375s%7CNONE%7CvVersion%7C5.2.0%7CMCSYNCSOP%7C411-19075"

# r = requests.get(url, cookies=cookies)

# pprint(r.text)

with open("test.json", 'r') as f:
    data = json.load(f)

print(data)
print(type(data))