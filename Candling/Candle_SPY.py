# %%
import sys
sys.path.append("/home/luke/Documents/GitHub/Data_Handling")

import numpy as np
import pandas as pd
import pandas_market_calendars as mcal
from Most_Recent_NBBO_Candling.Stock_NBBO_Candling import stock_NBBO_candle

# %%
#getting all market days from April 01 2022, to December 31 2022
nyse = mcal.get_calendar('NYSE')
dates = (nyse.schedule(start_date ='2022-04-01', end_date='2022-12-31'))['market_open'].to_list()

# %%
#Take the original raw SPY data, and candle it into the fixed_candle folder
path = "/srv/sqc/data/client-2378-luke-eq-taq/2022/" 

for num in range(len(dates)):
    date = dates[num].date().strftime('%Y%m%d')
    input_path = path + date + "/S/SPY.csv.gz"
    print(input_path)
    output_path = "/srv/sqc/volatility_exploration/fixed_candle/Stock_Data/" + date + ".csv"

    stock_NBBO_candle(input_path, output_path)


# %%
