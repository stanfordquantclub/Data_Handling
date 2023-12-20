from ib_insync import *
import datetime
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

earlier = datetime.datetime(2023, 11, 21, 7, 30, 0)

contract = Stock('SPY', 'SMART', 'USD')
bars = ib.reqHistoricalData(
    contract, endDateTime= earlier, durationStr='1800 S',
    barSizeSetting='1 secs', whatToShow='TRADES', useRTH=True)

# convert to pandas dataframe (pandas needs to be installed):
df = util.df(bars)
print(df)

print("hello world")