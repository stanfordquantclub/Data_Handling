import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, time, datetime, timedelta


# %%
path = "/srv/sqc/data/client-2378-luke-eq-taq/2022/20221201/S/SPY.csv.gz"
file = pd.read_csv(path)

# %%
start_time=time(9, 30, 0)
end_time=time(16, 0, 0)
