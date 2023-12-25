# %%
from ib_insync import *
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

# %%
ib = IB()

# %%
print(ib.accountSummary())
# %%
# getting all market days from January 2021, to November 2023
nyse = mcal.get_calendar('NYSE')
open_times = (nyse.schedule(start_date = '2021-01-01', end_date = '2023-11-28', tz = 'EST'))['market_open'].to_list()
close_times = (nyse.schedule(start_date = '2021-01-01', end_date = '2023-11-28', tz = 'EST'))['market_close'].to_list()


# %%
def retrieve(contract, endDateTime, durationStr, barSizeSetting, whatToShow):
    bars = ib.reqHistoricalData(contract, endDateTime=endDateTime,
                                durationStr=durationStr, barSizeSetting=barSizeSetting,
                                whatToShow=whatToShow, useRTH=True)
    
    return bars

# %%

def daysDataType(open_time, close_time, contract, whatToShow):
    cur_time = open_time + timedelta(minutes = 30)
    daysDf = util.df(retrieve(contract = contract, endDateTime=cur_time, durationStr='1800 S', 
               barSizeSetting='1 secs', whatToShow=whatToShow))

    while(cur_time != close_time):
        cur_time += timedelta(minutes = 30)
        daysDf = pd.concat([daysDf, 
                            util.df(retrieve(contract = contract, 
                                             endDateTime=cur_time, durationStr='1800 S', 
                                             barSizeSetting='1 secs', whatToShow=whatToShow))])
        
        daysDf.rename(columns = {"date": "date",
                                 "open": whatToShow + "_open",
                                 "high": whatToShow + "_high",
                                 "low": whatToShow + "_low",
                                 "close": whatToShow + "_close"})
    
    return daysDf

contract = Stock('SPY', 'SMART', 'USD')
newDf = daysDataType(open_times[0], close_times[0], contract, "ASK")

# %%
print(newDf)

# %%
