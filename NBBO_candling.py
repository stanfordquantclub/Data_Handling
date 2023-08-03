# %%
from datetime import date, time, datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%

path = "/srv/sqc/data/us-options-tanq/us-options-tanq-2022/20221201/S/SPY/SPY.20221201/SPY.P408.20221201.csv.gz"

df = pd.read_csv(path, compression='gzip')
columns = df.columns.values.tolist()

# %%
#get open interest
open_interest = df.iloc[0].tolist()[9]
print(open_interest)


# %%
start_time = time(9, 30, 0)
end_time = time(16, 0, 0)

# Convert to milliseconds
start_datetime = datetime.combine(date.today(), start_time) + timedelta(seconds=1)
start_time = int(start_time.strftime("%H%M%S")) * 1000

# Add 1 second to end time to include the last second
end_datetime = datetime.combine(date.today(), end_time) + timedelta(seconds=1)
end_time = int(end_datetime.strftime("%H%M%S")) * 1000

# FILTER OUT ITEMS FROM PRE-MARKET AND POST-MARKET
df["TimestampSec"] = df["Timestamp"] // 1000
df = df[(df["Timestamp"] >= start_time) & (df["Timestamp"] < end_time)]
total_seconds = int((end_datetime - start_datetime).total_seconds())

# %%
CLOCK_HOURS = np.array([int((start_datetime + timedelta(seconds=x)).time().strftime("%H%M%S")) for x in range(0, total_seconds)])

# %%
#filters asks and bids to only include those that are Firm Quote NBBO
df_nbbo = df[df['Action'] == "FQ NB"]
df_ask = df[df['Side'] == "A"]
df_bid = df[df['Side'] == "B"]

#filters asks and bids to be 
df_ask = df[df['Quantity'] >= 75]
df_bid = df[df['Quantity'] >= 75]


df_ask = (df_ask.loc[df_ask.groupby('TimestampSec').apply(lambda x: x.index[-1]).tolist()])[['TimestampSec', 'Side', 'Price', 'Quantity']]
df_bid = (df_bid.loc[df_bid.groupby('TimestampSec').apply(lambda x: x.index[-1]).tolist()])[['TimestampSec', 'Side', 'Price', 'Quantity']]

df_ask = df_ask.set_index(['Side', 'TimestampSec']).reindex(pd.MultiIndex.from_product([['A'], CLOCK_HOURS])).fillna(method='ffill').fillna(0)
df_bid = df_bid.set_index(['Side', 'TimestampSec']).reindex(pd.MultiIndex.from_product([['B'], CLOCK_HOURS])).fillna(method='ffill').fillna(0)


df_trade = df[df['Action'] == "T"]
df_trade = (df_trade.loc[df_trade.groupby('TimestampSec').apply(lambda x: x.index[-1]).tolist()])[['TimestampSec', 'Price', 'Quantity']]
# %%
print(df_trade)
#print(df_trade)
# %%
plt.plot(df_ask['Price'].tolist()[300:])
plt.show()
# %%
