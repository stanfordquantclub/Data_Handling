# %%
import sys
sys.path.append("/home/luke/Documents/GitHub/Data_Handling")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Training_Features.realized_volatiliity import realized_vol

# %%
path = "/srv/sqc/data/client-2378-luke-eq-taq/2022/20220401/S/SPY.csv.gz"
file = pd.read_csv(path)

# %%
candled_path = "/srv/sqc/volatility_exploration/NBBO_Candled/Most_Recent_Protocol/Stock_Data/20221215.csv"
candled_file = pd.read_csv(candled_path)
ask_list = candled_file['Ask'].tolist()
plt.plot(ask_list)
plt.show()
# %%


real_vol = realized_vol(ask_list, 600)
plt.plot(real_vol[:-600])
plt.show()


# %%
