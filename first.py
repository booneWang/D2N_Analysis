import pandas as pd
from datetime import datetime as dt

import_ds = pd.read_csv("D2N_Small.csv")
mark = pd.read_csv("Mark.csv")

ds = import_ds.merge(mark, left_on="Consumer", right_on="CustID")

# could change to "large"
ds = ds[ds.Mark == "small"]

ds_pos = ds[ds.Demand > 0]
ds_neg = ds[["Return", "Order Dt", "Order Nbr", "Sku Cd", "Rtn Qty"]][ds.Return < 0]
ds_pos1 = ds_pos.merge(ds_neg, how="left", left_on=["Order Nbr", "Sku Cd"], right_on=["Order Nbr", "Sku Cd"])

# ds_hr = ds_pos1[ds_pos1.Return_y < 0]
ds_hr = ds_pos1
ds_hr["gap"] = ds_hr.Demand + ds_hr.Return_y
# ds_hr.to_csv("ReturnAnalysis.csv")

d = ds_hr[ds_hr["Store Nm"] == "NIKE.COM"]
c = d.groupby(["Sku Cd", "Consumer"])["Sku Cd", "Consumer"].count()
c = c[c.Consumer == 2]

count = 0
total_demand = 0
customer_list = []
order_list = []
sku_list = []

for i in c.index:
    sku = i[0]
    customer = i[1]

    x = d[(d.Consumer == customer) & (d["Sku Cd"] == sku)]
    if (x["Return_y"].values[0] == x["Return_y"].values[0]) ^ (x["Return_y"].values[1] == x["Return_y"].values[1]):
        count += 1
        total_demand += x["Demand"].values[0]
        customer_list.append(x["Consumer"].values[0])
        order_list.append(x["Order Nbr"].values[0])
        sku_list.append(x["Sku Cd"].values[0])

        print("{0} - {1}".format(count, total_demand))

cc = pd.DataFrame(sku_list, columns=["col"])
cc.groupby("col")["col"].count()
