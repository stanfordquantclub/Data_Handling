# %%
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import as_strided


# %%
path = "/srv/sqc/volatility_exploration/fixed_candle/Stock_Data/20220401.csv"
df = pd.read_csv(path)

# %%
import matplotlib.pyplot as plt
price = df['Price'].tolist()
plt.plot(price)
plt.show()

# %%

array = np.array(price)

window_length = 300
step_size = 1

shape = (array.size - window_length + 1, window_length)
strides = (array.strides[0] * step_size, array.strides[0])

result = np.log(as_strided(array, shape=shape, strides=strides))
