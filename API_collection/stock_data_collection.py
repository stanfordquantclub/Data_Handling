# %%
from ib_insync import *
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal
import time

util.startLoop()

# %%
# getting all market days from January 2021, to November 2023
nyse = mcal.get_calendar('NYSE')
open_times = (nyse.schedule(start_date = '2021-01-01', end_date = '2023-12-25', tz = 'EST'))['market_open'].to_list()
close_times = (nyse.schedule(start_date = '2021-01-01', end_date = '2023-12-25', tz = 'EST'))['market_close'].to_list()

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

def get_stock_df(contract, start_dateTime_list, endDateTime_list, durationStr, barSizeSetting, out_path):
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
            
            # get implied volatility data
            iv_df = get_stock_info(contract, endDateTime, durationStr, barSizeSetting, "OPTION_IMPLIED_VOLATILITY")
            
            # rename iv columns (open, high, low, close) --> (iv_open, iv_high, iv_low, iv_close)
            iv_df = iv_df.rename(columns = {"date": "date",
                                    "open": "iv_open",
                                    "high": "iv_high",
                                    "low": "iv_low",
                                    "close": "iv_close"})
            
            # get trade data
            trade_df = get_stock_info(contract, endDateTime, durationStr, barSizeSetting, "TRADES")

            # rename trade columns (open, high, low, close) --> (trade_open, trade_high, trade_low, trade_close)
            trade_df = trade_df.rename(columns = {"date": "date",
                                    "open": "trade_open",
                                    "high": "trade_high",
                                    "low": "trade_low",
                                    "close": "trade_close"})
            
            # get historical volatility data
            hv_df = get_stock_info(contract, endDateTime, durationStr, barSizeSetting, "HISTORICAL_VOLATILITY")

            # rename hv columns (open, high, low, close) --> (hv_open, hv_high, hv_low, hv_close)
            hv_df = hv_df.rename(columns = {"date": "date",
                                    "open": "hv_open",
                                    "high": "hv_high",
                                    "low": "hv_low",
                                    "close": "hv_close"})

            # concatenate ask and bid data and remove redundant columns
            df = pd.concat([ask_df, bid_df, iv_df, trade_df, hv_df], axis=1)
            df = df.loc[:,~df.columns.duplicated()].drop(columns = ["barCount", "average", "volume"])
            df.to_csv(out_path + "/" + str(endDateTime.strftime("%Y%m%d")) + ".csv")


# %%
contract = Stock('SPY', 'SMART', 'USD')
print(len(close_times))

# %%
def partition_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# %%
partitioned_open_times = list(partition_list(open_times, 12))
partitioned_close_times = list(partition_list(close_times, 12))

interval = 11 * 60


for i in range(41, len(partitioned_open_times)):
    start_dateTime_list = partitioned_open_times[i]
    endDateTime_list = partitioned_close_times[i]
    get_stock_df(contract, start_dateTime_list, endDateTime_list, '1 D', '1 min', out_path = "/Users/lukepark/Documents/SPY_STOCK_DATA/Min_Res")
    print(f'Finished {i}th iteration out of {len(partitioned_open_times)}')
    time.sleep(interval)

ib.disconnect()
