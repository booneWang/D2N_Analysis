import pandas as pd

path = "C:\\Users\\bwan19\\Boone_Document\# Nwork\$Projects\Digital G2N Analysis\\05. Analysis\D2N LAST 5 SEASON DATA\Original\{}.csv"
filenames = ["SP18_new", "HO17", "SU17", "FA17", "SP17"]

file = path.format(filenames[0])
ds = pd.read_csv(file).head(0)

for filename in filenames:
    file = path.format(filename)
    ds = pd.concat([ds, pd.read_csv(file)])

# Test
ds["Net Demand Amt"].sum()
ds.to_csv(path.format("haha"))
