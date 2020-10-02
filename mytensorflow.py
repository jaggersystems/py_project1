import numpy as np
import functions as fn

import tensorflow as tf
from tensorflow import keras

# Date[0], Time[1], Open[2], High[3], Low[4], Close[5], Volume[6]
import csv
with open('GBPUSDH4_small.csv', "r", newline='') as csv_file:
    data = list(csv.reader(csv_file))
csv_file.close()


# creating an empty 1d array of int type
npdata = np.empty((0, 1), int)   # 0,2 or 2d etc.

# using np.append() to add rows to array
i = 0
while i <= len(data)-1:
    c_open = float(data[i][2])
    c_high = float(data[i][3])
    c_low = float(data[i][4])
    c_close = float(data[i][5])

    candle_bull = fn.is_bull_candle(c_open, c_close)
    candle_range = fn.calculate_range(c_high, c_low)
    candle_high = fn.calculate_high(c_open, c_high, c_low, c_close)
    candle_body = fn.calculate_body(c_open, c_high, c_low, c_close)
    candle_low = fn.calculate_low(c_open, c_high, c_low, c_close)

    candle_id = str(format(candle_high, "02")) + "" + \
                str(format(candle_body, "02")) + "" + \
                str(format(candle_low, "02"))

    npdata = np.append(npdata, np.array([[str(candle_id)]]), axis=0)

    i += 1


# Get a tuple of unique values & their frequency in numpy array
# uniqueValues, indicesList, occurCount, = np.unique(nparray, return_index=True, return_counts=True)

