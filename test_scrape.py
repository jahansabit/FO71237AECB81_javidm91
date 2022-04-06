import http.client

conn = http.client.HTTPSConnection("api.scrapingant.com")

headers = {
    'x-api-key': "0604022f0d274c569d487cc4782df5c5"
}

conn.request("GET", "/v1/general?url=https%3A%2F%2Fwww.pccomponentes.com%2Fasus-geforce-gtx-1660-super-oc-dual-6gb-gddr6", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))