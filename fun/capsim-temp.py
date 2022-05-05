import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

emergency_loan = [ 
    0,
    3486595,
    0,
    7348407,
    0,
    0,
    0,
    0,
]
sales = [
    50071484,
    59397571,
    81219860,
    43646331,
    44265335,
    40783690,
    68525954,
    84595161,
]
profit = [
    4121864,
    -749814,
    4415137,
    -4931853,
    4180849,
    -2304659,
    3980928,
    6402968,
]
stock_price = [
    17.67,
    9.37,
    16.19,
    1.15,
    11.28,
    9.52,
    14.45,
    27.57,
]
units_sold = [
    1252,
    1399,
    1919,
    1006,
    1019,
    994,
    2003,
    2550,
]
high_tech_market_share = [
    22,
    32,
    40,
    23,
    18,
    11,
    14,
    10,
]
total_market_share = [
    15.4,
    15.2,
    18.4,
    8.5,
    7.5,
    6.5,
    11.4,
    12.7,
]

df = pd.DataFrame(data=[emergency_loan, sales, profit,
    stock_price, units_sold, high_tech_market_share, total_market_share]).transpose()
df.columns = ["Emergency Loan", "Sales", "Profit", "Stock Price", "Units Sold", "High Tech Market Share", "Total Market Share"]
df.index = [idx+1 for idx in df.index]
print(df)
df[["Sales", "Emergency Loan"]].plot()
plt.title("Sales related to Profit and Emergency Loans per Round", fontsize=16)
plt.ylabel("$", fontsize=16)
plt.xlabel("Round", fontsize=16)
plt.ticklabel_format(style="plain", axis="y")
plt.show()
