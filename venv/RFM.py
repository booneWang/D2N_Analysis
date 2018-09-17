import pandas as pd
import numpy as np

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
