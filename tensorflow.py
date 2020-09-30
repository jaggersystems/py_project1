import pandas as pd
import numpy as np

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf

abalone_train = pd.read_csv(
    "EURUSD-big.csv", header=None,
    names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])

abalone_train.head()