import pandas as pd

path = "C:\\Users\\bwan19\\Boone_Document\# Nwork\$Projects\Digital G2N Analysis\\05. Analysis\Raw Data\Original\{}.csv"
filename = "618"
file = path.format(filename)
ds = pd.read_csv(file)
saving_file = True

# Preconditioning the dataset
# ds = ds[ds["Store Nm"] == "NIKE.COM"]

ds["Order Dt"] = pd.to_datetime(ds["Order Dt"])

# ---Brief------------------------------------------------------------
# Period
start_date = ds["Order Dt"].min()
end_date = ds["Order Dt"].max()
print("Time Period of the Dataset:\n{}\n{}\n\n".format(start_date, end_date))

# Total Order Number
ds_order = ds.groupby(ds["ORDER_NBR"])
total_order_number = ds_order.count().count()[0]

# Buy Order Number
ds_order = ds.groupby(ds[ds["NET REVENUE"] >= 0]["ORDER_NBR"])
buy_order_number = ds_order.count().count()[0]

# Buy Order Number
ds_order = ds.groupby(ds[ds["NET REVENUE"] < 0]["ORDER_NBR"])
return_order_number = ds_order.count().count()[0]

# Display Order
print("Total Order: {:>8,} \n  Buy Order: {:>8,} \n  Rtn Order: {:>8,}\n".format(total_order_number, buy_order_number,
                                                                                 return_order_number))


net_demand = ds["Net Demand Amt"].sum()
net_revenue = ds["NET REVENUE"].sum()

print("Net Demand:${:>16,.2f} \nNet Revenue:${:>15,.2f}\nReturn:${:>20,.2f}\n".format(net_demand, net_revenue,
                                                                                      net_demand - net_revenue))

print("Buy$ per Order:{:>13,.2f}\nReturn$ per order:{:>10,.2f}".format(net_demand / buy_order_number,
                                                                       (
                                                                               net_demand - net_revenue) / return_order_number))
# -------------------------------------------------------------------

# Calculate the Return Days--------------------------------------------
# Have the Return Record
ds_return = ds[["Consumer", "Order Dt", "ORDER_NBR", "SKU_CD"]][ds["NET REVENUE"] < 0]
# Have the Buy Record
ds_buy = ds[ds["NET REVENUE"] > 0]
ds_buy["Rtn Days"] = 0
# Join the buy and Return by Consumer + Order + SKU
ds_buy = ds_buy.merge(ds_return, how="left", on=["Consumer", "ORDER_NBR", "SKU_CD"])
# Return Days = Return Date - Buy Date
ds_buy["Rtn Days"] = ds_buy["Order Dt_y"] - ds_buy["Order Dt_x"]

# Change timedelta to num of days!!!
ds_buy["Rtn Days"] = ds_buy["Rtn Days"].map(lambda x: x.days)

# Cleansing - Remove blank (no return)
ds_buy = ds_buy[ds_buy["Rtn Days"] >= 0][["ORDER_NBR", "SKU_CD", "Rtn Days"]]
# Cleansing - Remove Duplicated
ds_buy = ds_buy.groupby(["ORDER_NBR", "SKU_CD"])["Rtn Days"].mean()
# Cleansing - Reset index
ds_buy = ds_buy.reset_index()

ds_with_rtn_days = ds.merge(ds_buy, how="left", on=["ORDER_NBR", "SKU_CD"])

# # Save to File
# if saving_file:
#     file = path.format(filename + "_withoutReturnDays")
#     ds.to_csv(file)

# Save to File
if saving_file:
    file = path.format(filename + "_withReturnDays")
    ds_with_rtn_days.to_csv(file, encoding="utf16")
# -------------------------------------------------------------------

# Consumer by agg Demand------------------------------------------------
ds_consumer = ds.groupby(["Consumer"])["Net Demand Amt"].sum()
ds_consumer = ds_consumer.reset_index()
ds_consumer["Demand Zone"] = round(ds_consumer["Net Demand Amt"] / 100, 0) * 100

if saving_file:
    filename += "_ConsumerOnDemand"
    file = path.format(filename)
    ds_consumer.to_csv(file)
# -------------------------------------------------------------------

# 关联分析，指定一个sytle，找到搭配组多的Style-------------------------------

style = "378037"
ds["Style"] = ds["SKU_CD"].map(lambda x: x[0:6])
field = "Consumer"
top = 5

# Order Based
orders = ds[ds["Style"] == style]["ORDER_NBR"]

ds_products = ds[ds["ORDER_NBR"].isin(orders)][["Styl Nm", "Style", field]]
ds_products_group = ds_products.groupby(["Styl Nm", "Style"])[field].nunique()
ds_products_group = ds_products_group.reset_index()
ds_products_group = ds_products_group.sort_values(by=field, ascending=False)
print("\n\n--Same Order--\n{}".format(ds_products_group.head(top)))

# Consumer Based
orders = ds[ds["Style"] == style]["Consumer"]

ds_products = ds[ds["Consumer"].isin(orders)][["Styl Nm", "Style", field]]
ds_products_group = ds_products.groupby(["Styl Nm", "Style"])[field].nunique()
ds_products_group = ds_products_group.reset_index()
ds_products_group = ds_products_group.sort_values(by=field, ascending=False)
print("\n\n--Same Consumer--\n{}".format(ds_products_group.head(top)))

# -------------------------------------------------------------------
