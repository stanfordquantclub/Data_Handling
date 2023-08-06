# %%
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import as_strided

# Returns a list of the realized_volatility given the pricing data and the lookback windwo
def realized_vol(price, window):
    array = np.array(price)
    window_length = window
    step_size = 1

    shape = (array.size - window_length + 1, window_length)
    strides = (array.strides[0] * step_size, array.strides[0])
    array = as_strided(array, shape=shape, strides=strides)

    # Check for zero values in the original array
    if np.any(array == 0):
        print("Warning: Zero values found in the array. Replacing with a small positive number.")
        array[array == 0] = 1e-10  # Replace zeros with a small positive number, or handle as needed

    # Taking the logarithm of the array
    array = np.log(array)

    # Log difference in prices 
    differences = array[1:] - array[:-1]
    
    # Finds realized_var, sum of log differences in prices over each time frame
    realized_var = differences ** 2
    sum = np.sum(realized_var, axis=1)
    print(sum)

    # Find the realized_vol by square rooting realized_var
    realized_vol = np.sqrt(sum) * 100

    # Pad the real_vol by the window length
    real_vol = np.concatenate((np.zeros(window_length), realized_vol))

    return real_vol
