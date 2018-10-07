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


ds = pd.read_csv("CONSADDR.csv", encoding="utf8")
ds["lat"] = 0
ds['lng'] = 0

# 100 sample for test purpose
ds = ds.head(3000)
# ds.reset_index(inplace=True)
# del ds["index"]

for indexs in ds.index:
    address = ds.loc[indexs]["ADDR"]

    lat, lng = GetCoordinateOnGaodei(address)

    # 维度
    ds.iloc[indexs, 4] = lat
    # 经度
    ds.iloc[indexs, 5] = lng

    if indexs % 100 == 0:
        print(indexs)

ds.to_excel("CONSADDRwithLLGaode.xls", encoding="utf8")

print("done")
