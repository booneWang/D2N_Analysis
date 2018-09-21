import pandas as pd
import numpy as np
import datetime as dt
from sklearn.cluster import KMeans

ds = pd.read_csv("")

# Get Demand only
ds = ds[ds["NET REVENUE"] > 0]
ds["Order Dt"] = pd.to_datetime(ds["Order Dt"])

# Get Sample data only
dssample = ds

group = dssample.groupby("Consumer")
agg = group.agg({"Net Demand Amt": "sum", "Order Dt": "max", "Order Nbr": "nunique"})

agg = agg.reset_index()
agg.to_csv("C:\\Users\\bwan19\\Desktop\\RMF.csv")

# Further Process
ds = pd.read_csv("C:\\Users\\bwan19\\Desktop\\RMF Analysis\\RMF.csv")
ds["Order Dt"] = pd.to_datetime(ds["Order Dt"])
standardDate = dt.datetime(2018, 6, 30)


# Set the rule of recency
def tag_recency(x):
    if x <= 2: return "1 - 3"
    if x >= 3 and x <= 5: return "4 - 6"
    if x >= 6 and x <= 8: return "7 - 9"
    if x >= 9: return "10 - 12"


# Set Recency
ds["Recency"] = ds["Order Dt"]
# Set Recency as days
ds["Recency"] = ds["Recency"].apply(lambda x: (standardDate - x).days)
# Set Recency as months
ds["Recency"] = ds["Recency"].apply(lambda x: x // 30)
ds["Recency"] = ds["Recency"].apply(tag_recency)

# Set Frequency
ds["Frequency"] = ds["Order Nbr"]
# group >= 5 as 5
ds["Frequency"] = ds["Frequency"].apply(lambda x: 5 if x >= 5 else x)

ds.to_csv("C:\\Users\\bwan19\\Desktop\\RMF1.csv")

# 聚类
km = KMeans()
km.fit(ds)
