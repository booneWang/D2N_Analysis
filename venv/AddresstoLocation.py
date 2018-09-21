import pandas as pd
import requests
import json

url_template = "http://api.map.baidu.com/geocoder/v2/?address={0}&output=json&ak={1}"
myAK = "RmTWSrlP7ijaCUadIUArGrmXv9ZsKgSg"

ds = pd.read_csv("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\AddressTest.csv", encoding="gbk")
ds["lat"] = 0
ds['lng'] = 0

for indexs in ds.index:
    address = "上海市" + ds.loc[indexs]["地址"]

    url = url_template.format(address, myAK)
    request = requests.get(url)
    js = json.loads(request.text)

    # 维度
    ds.iloc[indexs, 5] = js["result"]["location"]["lat"]
    # 经度
    ds.iloc[indexs, 6] = js["result"]["location"]["lng"]

ds.to_csv("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\AddressTestwithlocation.csv")
