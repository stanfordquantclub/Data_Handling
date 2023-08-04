Objectives:

1. Recandle options data to use NBBO price data
    - filters asks and bids for only those that are Firm Quote NBBO
    - filters asks and bids for only those that have size lots greater than 75 (liquidity 
      purposes)
    - added open interest to better evaluate liquidity

2. Recandle underlying SPY data to use NBBO price data
    - Same Process as the options data

3. Add features for training
    - Add how many strikes away from underlying the contract is
        - positive values means ITM, negative values means OTM
    - Add realized_vol with 10 min, 20 min, 30 min windows
    - Add count of d/dprice over different window sizes to data
        - This is to gauge whether or not volatility is being affected by choppy 
          oscillating price movement
    - Add count of d/dprice that crosses certain threshold over different window sizes to 
      data
