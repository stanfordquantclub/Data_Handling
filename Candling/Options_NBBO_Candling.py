from datetime import date, time, datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def options_NBBO_candle(file_path, output_path, start_time=time(9, 30, 0), end_time=time(16, 0, 0)):
    df = pd.read_csv(file_path, compression='gzip')
    open_interest = df.iloc[0].tolist()[9]
    contract_type = df.iloc[0].tolist()[2]

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


    CLOCK_HOURS = np.array([int((start_datetime + timedelta(seconds=x)).time().strftime("%H%M%S")) for x in range(0, total_seconds)])

    #filters asks and bids to only include those that are Firm Quote NBBO
    df_nbbo = df[df['Action'] == "FQ NB"]
    df_ask = df[df['Side'] == "A"]
    df_bid = df[df['Side'] == "B"]

    #filters asks and bids where quantity is at least 75
    df_ask = (df[df['Quantity'] >= 75])
    df_bid = df[df['Quantity'] >= 75]

    #getting the last NBBO ask price of a given second group, along with its associated quantity
    df_ask = (df_ask.loc[df_ask.groupby('TimestampSec')
                        .apply(lambda x: x.index[-1]).tolist()]
                        [['TimestampSec', 'Side', 'Price', 'Quantity']]
                        .set_index(['Side', 'TimestampSec'])
                        .reindex(pd.MultiIndex.from_product([['A'], CLOCK_HOURS]))
                        .fillna(method='ffill').fillna(0)
                        .rename(columns={"TimestampSec": "Timestamp", "Price": "Ask", "Quantity": "AskQty"}))
    df_ask.reset_index(drop=True, inplace=True)
    df_ask.columns = df_ask.columns.get_level_values(0)

    #getting the last NBBO bid price of a given second group, along with its associated quantity
    df_bid = (df_bid.loc[df_bid.groupby('TimestampSec')
                        .apply(lambda x: x.index[-1]).tolist()]
                        [['TimestampSec', 'Side', 'Price', 'Quantity']]
                        .set_index(['Side', 'TimestampSec'])
                        .reindex(pd.MultiIndex.from_product([['B'], CLOCK_HOURS]))
                        .fillna(method='ffill').fillna(0)
                        .unstack(level=0)
                        .rename(columns={"TimestampSec": "Timestamp", "Price": "Bid", "Quantity": "BidQty"})
                        )
    df_bid.reset_index(drop=True, inplace=True)
    df_bid.columns = df_bid.columns.get_level_values(0)

    #getting the volume and prices when trades do occur
    df_trade = df[df['Action'] == 'T']
    df_volume = (df_trade.groupby(df_trade['TimestampSec'])['Quantity']
                                .sum()
                                .to_frame()
                                .reindex(CLOCK_HOURS)
                                .fillna(method='ffill').fillna(0)
                                .rename(columns={"Quantity": "TradeVolume"}))
    df_volume.reset_index(drop=True, inplace=True)

    df_price = (df_trade.loc[df_trade.groupby('TimestampSec')
                        .apply(lambda x: x.index[-1]).tolist()]
                        [['TimestampSec', 'Action', 'Price', 'Quantity']]
                        .set_index(['Action', 'TimestampSec'])
                        .reindex(pd.MultiIndex.from_product([['T'], CLOCK_HOURS]))
                        .fillna(method='ffill').fillna(0)
                        .rename(columns={"TimestampSec": "Timestamp", "Quantity": "TotalVolume"}))
    df_price.reset_index(drop=True, inplace=True)
    df_price.columns = df_price.columns.get_level_values(0)

    #getting the Underlying Ask Price
    df_under_ask = (df.groupby(df['TimestampSec'])['UnderAskPrice']
                    .last()
                    .to_frame()
                    .reindex(CLOCK_HOURS)
                    .fillna(method='ffill').fillna(0))
    df_under_ask.reset_index(drop=True, inplace=True)

    #getting the Underlying Bid Price
    df_under_bid = (df.groupby(df['TimestampSec'])['UnderBidPrice']
                    .last()
                    .to_frame()
                    .reindex(CLOCK_HOURS)
                    .fillna(method='ffill').fillna(0))
    df_under_bid.reset_index(drop=True, inplace=True)

    #getting the number of strikes from underlying
    mult = 1 if contract_type == "P" else -1
    strike_price = round(float(path.split('/')[-1].split('.')[1][1:]), 2)
    num_strikes = round((df_under_ask['UnderAskPrice'] - strike_price) * mult, 2) 

    #getting the open interest
    OI = np.full(len(CLOCK_HOURS), open_interest)

    df_all = pd.DataFrame({'Timestamp': CLOCK_HOURS, 'OI': OI, 'Num_strikes': num_strikes})
    df_candled = pd.concat([df_all, df_under_ask, df_under_bid, df_ask, df_bid, df_volume, df_price], axis=1)
    df_candled.to_csv(output_path)

path = "/srv/sqc/data/us-options-tanq/us-options-tanq-2022/20221201/S/SPY/SPY.20221201/SPY.P408.20221201.csv.gz"
out_path = "/srv/sqc/volatility_exploration/fixed_candle/blah.csv"

options_NBBO_candle(path, out_path)
 
