import pandas as pd

path = "C:\\Users\\bwan19\\Boone_Document\# Nwork\$Projects\Digital G2N Analysis\\05. Analysis\Raw Data\Original\{}.csv"
filenames = ["SU18", "SP18_new", "HO17", "FA17"]

file = path.format(filenames[0])
ds = pd.read_csv(file).head(0)

for filename in filenames:
    file = path.format(filename)
    ds = pd.concat([ds, pd.read_csv(file)])

# Test
ds["Net Demand Amt"].sum()
# ds.to_csv(path.format("FA17_to_SP18"))


#---------------------------------------
sku = pd.read_csv("c:\\sku.csv")
ds = ds[ds["Sku Cd"].isin(sku["sku"])]