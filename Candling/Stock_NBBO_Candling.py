# %%
from datetime import date, time, datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
def stock_NBBO_candle(file_path, output_path, start_time=time(9, 30, 0), end_time=time(16, 0, 0)):
    df = pd.read_csv(file_path, compression='gzip')

    # Convert to milliseconds
    start_datetime = datetime.combine(date.today(), start_time) + timedelta(seconds=1)
    start_time = int(start_time.strftime("%H%M%S")) * 1000

    # Add 1 second to end time to include the last second
    end_datetime = datetime.combine(date.today(), end_time) + timedelta(seconds=1)
    end_time = int(end_datetime.strftime("%H%M%S")) * 1000

    # FILTER OUT ITEMS FROM PRE-MARKET AND POST-MARKET
    df["TimestampSec"] = pd.to_numeric(df["Timestamp"].str.slice(stop=8).str.replace(':', ''))
    df = df[(df["TimestampSec"] >= start_time // 1000) & (df["TimestampSec"] < end_time // 1000)]
    total_seconds = int((end_datetime - start_datetime).total_seconds())

    CLOCK_HOURS = np.array([int((start_datetime + timedelta(seconds=x)).time().strftime("%H%M%S")) for x in range(0, total_seconds)])

    #filters asks and bids to only include those that are Firm Quote NBBO

    df_ask = df[(df['EventType'] == "QUOTE ASK NB") & (df['Quantity'] >= 250)]
    df_bid = df[(df['EventType'] == "QUOTE BID NB") & (df['Quantity'] >= 250)]

    #getting the last NBBO ask price of a given second group, along with its associated quantity
    df_ask = (df_ask.loc[df_ask.groupby('TimestampSec')
                        .apply(lambda x: x.index[-1]).tolist()]
                        [['TimestampSec', 'EventType', 'Price', 'Quantity']]
                        .set_index(['EventType', 'TimestampSec'])
                        .reindex(pd.MultiIndex.from_product([['QUOTE ASK NB'], CLOCK_HOURS]))
                        .fillna(method='ffill').fillna(0)
                        .rename(columns={"TimestampSec": "Timestamp", "Price": "Ask", "Quantity": "AskQty"}))
    df_ask.reset_index(drop=True, inplace=True)
    df_ask.columns = df_ask.columns.get_level_values(0)

    #getting the last NBBO bid price of a given second group, along with its associated quantity
    df_bid = (df_bid.loc[df_bid.groupby('TimestampSec')
                        .apply(lambda x: x.index[-1]).tolist()]
                        [['TimestampSec', 'EventType', 'Price', 'Quantity']]
                        .set_index(['EventType', 'TimestampSec'])
                        .reindex(pd.MultiIndex.from_product([['QUOTE BID NB'], CLOCK_HOURS]))
                        .fillna(method='ffill').fillna(0)
                        .unstack(level=0)
                        .rename(columns={"TimestampSec": "Timestamp", "Price": "Bid", "Quantity": "BidQty"})
                        )
    df_bid.reset_index(drop=True, inplace=True)
    df_bid.columns = df_bid.columns.get_level_values(0)

    #getting the volume and prices when trades do occur
    df_trade = df[df['EventType'] == 'TRADE']
    df_volume = (df_trade.groupby(df_trade['TimestampSec'])['Quantity']
                                .sum()
                                .to_frame()
                                .reindex(CLOCK_HOURS)
                                .fillna(method='ffill').fillna(0)
                                .rename(columns={"Quantity": "TradeVolume"}))
    df_volume.reset_index(drop=True, inplace=True)

    df_price = (df_trade.loc[df_trade.groupby('TimestampSec')
                        .apply(lambda x: x.index[-1]).tolist()]
                        [['TimestampSec', 'EventType', 'Price']]
                        .set_index(['EventType', 'TimestampSec'])
                        .reindex(pd.MultiIndex.from_product([['TRADE'], CLOCK_HOURS]))
                        .fillna(method='ffill').fillna(0)
                        .rename(columns={"TimestampSec": "Timestamp"}))
    df_price.reset_index(drop=True, inplace=True)
    df_price.columns = df_price.columns.get_level_values(0)

    df_all = pd.DataFrame({'Timestamp': CLOCK_HOURS})
    df_candled = pd.concat([df_all, df_ask, df_bid, df_price, df_volume], axis=1)
    df_candled.to_csv(output_path)

# %%
file_path = "/srv/sqc/data/client-2378-luke-eq-taq/2022/20220401/S/SPY.csv.gz"
output_path = "/srv/sqc/volatility_exploration/fixed_candle/stock.csv"

stock_NBBO_candle(file_path, output_path)