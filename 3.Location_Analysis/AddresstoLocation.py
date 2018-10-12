import pandas as pd
import requests
import json


def GetCoordinateOnBaidu(address):
    url_template = "http://api.map.baidu.com/geocoder/v2/?address={0}&output=json&ak={1}"
    myAK = "RmTWSrlP7ijaCUadIUArGrmXv9ZsKgSg"
    if address != "":
        url = url_template.format(address, myAK)
        request = requests.get(url)
        js = json.loads(request.text)

        if js["status"] == 0:
            lat, lng = js["result"]["location"]["lat"], js["result"]["location"]["lng"]

            return float(lat), float(lng)
        else:
            return 0, 0


def GetCoordinateOnGaodei(address):
    url_template = "https://restapi.amap.com/v3/geocode/geo?address={0}&key={1}&output=JSON"
    key = "6db69300890974d6b83b474efc6ea792"
    if address != "":
        url = url_template.format(address, key)
        request = requests.get(url)
        js = json.loads(request.text)

        # check result 1:successful, 0:failed
        if js["status"] == "1" and js["count"] != "0":
            lng, lat = js["geocodes"][0]["location"].split(",")

            return float(lat), float(lng)
        else:
            return 0, 0


ds = pd.read_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\201808ConsumerList.xlsx",
                   encoding="utf8")
ds["lat"] = 0
ds['lng'] = 0

# 100 sample for test purpose
# ds = ds.head(5000)
# ds.reset_index(inplace=True)
# del ds["index"]

# How many Cycle need to run
ds = ds.loc[5000:8000]

for i in ds.index:
    address = ds.loc[i]["Addr"]
    address = "上海市" + address

    lat, lng = GetCoordinateOnGaodei(address)

    # 维度
    ds.iloc[i - 5000, 2] = lat
    # 经度
    ds.iloc[i - 5000, 3] = lng

    if i % 100 == 0:
        print(i)

ds.to_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\201808ConsumerList_20181012.xlsx", encoding="utf8")

print("done")