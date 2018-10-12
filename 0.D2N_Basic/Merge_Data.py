import pandas as pd

path = "C:\\Users\\bwan19\\Boone_Document\# Nwork\$Projects\Digital G2N Analysis\\05. Analysis\Raw Data\Original\FA18\\{}.csv"
filenames = ["FA18NIKE_withReturnDays",
             "FA18TMALL_withReturnDays"]

# Load the small field list
dsFieldList = pd.read_csv("0.D2N_Basic\\FieldList.csv")

# initilization
file = path.format(filenames[0])
ds = pd.read_csv(file, encoding="utf16").head(0)

# Cycle for load all raw data
for filename in filenames:
    file = path.format(filename)
    ds = pd.concat([ds, pd.read_csv(file, encoding="utf16")])

# Trim raw data and keep the small one
dssmall = ds[list(dsFieldList["Field"])]

# Test
dssmall["Net Demand Amt"].sum()

# Export
# ds.to_csv(path.format("FA17_to_SP18"))


# ---------------------------------------
