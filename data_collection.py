# %%
from ib_insync import *
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

util.startLoop()

# %%
# getting all market days from January 2021, to November 2023
nyse = mcal.get_calendar('NYSE')
open_times = (nyse.schedule(start_date = '2021-01-01', end_date = '2023-11-28', tz = 'EST'))['market_open'].to_list()
close_times = (nyse.schedule(start_date = '2021-01-01', end_date = '2023-11-28', tz = 'EST'))['market_close'].to_list()

# %%
ib = IB()
ib.connect('127.0.0.1', 4002, clientId=1)

# %%
def get_stock_info(contract, endDateTime, durationStr, barSizeSetting, whatToShow):
    bars = ib.reqHistoricalData(
        contract, endDateTime=endDateTime, durationStr=durationStr,
        barSizeSetting=barSizeSetting, whatToShow=whatToShow, useRTH=True)
    df = util.df(bars)
    return df

def get_stock_df(contract, start_dateTime_list, endDateTime_list, durationStr, barSizeSetting):
    if barSizeSetting == '1 min':
        # get ask data
        for endDateTime in endDateTime_list:
            ask_df = get_stock_info(contract, endDateTime, durationStr, barSizeSetting, "ASK")

            # rename ask columns (open, high, low, close) --> (ask_open, ask_high, ask_low, ask_close)
            ask_df = ask_df.rename(columns = {"date": "date",
                                    "open": "ask_open",
                                    "high": "ask_high",
                                    "low": "ask_low",
                                    "close": "ask_close"})
            
            # get bid data
            bid_df = get_stock_info(contract, endDateTime, durationStr, barSizeSetting, "BID")

            # rename bid columns (open, high, low, close) --> (bid_open, bid_high, bid_low, bid_close)
            bid_df = bid_df.rename(columns = {"date": "date",
                                    "open": "bid_open",
                                    "high": "bid_high",
                                    "low": "bid_low",
                                    "close": "bid_close"})
            
            # concatenate ask and bid data and remove redundant columns
            df = pd.concat([ask_df, bid_df], axis=1)
            df = df.loc[:,~df.columns.duplicated()].drop(columns = ["barCount", "average", "volume"])
            return df


# %%
contract = Stock('SPY', 'SMART', 'USD')
df = get_stock_df(contract, open_times[0:10], close_times[0:10], '1 D', '1 min')
print(df)
