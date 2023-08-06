# %%
import sys
sys.path.append("/home/luke/Documents/GitHub/Data_Handling")

import numpy as np
import pandas as pd
from Most_Recent_NBBO_Candling.Options_NBBO_Candling import options_NBBO_candle
from Most_Recent_NBBO_Candling.Stock_NBBO_Candling import stock_NBBO_candle
from Training_Features.realized_volatiliity import realized_vol
from Training_Features.unidirectional_change import maxLoss_list, maxProfit_list

# %%

# Options are correlated with each other
path = "/srv/sqc/volatility_exploration/batches_files.csv"
dec_01_files = pd.read_csv(path)['20221201'].tolist()

# %%
prices_list = []

for file in dec_01_files:
    path = "/srv/sqc/data/us-options-tanq/us-options-tanq-2022/20221201/S/SPY" + file
    