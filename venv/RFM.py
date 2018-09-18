import pandas as pd
import numpy as np
import datetime as dt

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
ds = pd.read_csv("C:\\Users\\bwan19\\Desktop\\RMF.csv")
ds["Order Dt"] = pd.to_datetime(ds["Order Dt"])
standardDate = dt.datetime(2018, 6, 30)

# Set Recency
ds["Recency"] = ds["Order Dt"]
# Set Recency as days
ds["Recency"] = ds["Recency"].apply(lambda x: (standardDate - x).days)
# Set Recency as months
ds["Recency"] = ds["Recency"].apply(lambda x: x // 30)

# Set Frequency
ds["Frequency"] = ds["Order Nbr"]
# group >= 5 as 5
ds["Frequency"] = ds["Frequency"].apply(lambda x: 5 if x >= 5 else x)

ds.to_csv("C:\\Users\\bwan19\\Desktop\\RMF1.csv")
