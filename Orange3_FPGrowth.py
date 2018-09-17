import orangecontrib.associate.fpgrowth as oaf
import pandas as pd
import json

# by = "Order Nbr"
by = "Consumer"

ds_small = ds.groupby([by, "Sku Cd"])["Styl Nm"].count()
ds_small = ds_small.reset_index()
T = []
count = 0

for i in ds_small[by].unique():
    ds_by = ds_small[ds_small[by] == i]
    t = []

    for j in ds_by["Sku Cd"]:
        t.append(j)
    T.append(t)

    count += 1
    if count % 1000 == 0:
        print(count)

# Save the list to file
j = json.dumps(T)
with open("data by consumer.txt", "w") as file:
    file.write(j)
# Read file to ilst
with open("data.txt", "r") as file:
    l = file.read()
    l = json.loads(l)
