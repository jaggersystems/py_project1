import numpy as np
import functions as fn

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, Flatten, Dense, Concatenate


# Date[0], Time[1], Open[2], High[3], Low[4], Close[5], Volume[6]
import csv
with open('EURUSD.csv', "r", newline='') as csv_file:
    data = list(csv.reader(csv_file))
csv_file.close()


# creating an empty 1d array of int type
npdata = np.empty((5,0), int)   # 0,2 or 2d etc.

# using np.append() to add rows to array
i = 0
while i <= len(data)-2:
    c_open = float(data[i][2])
    c_high = float(data[i][3])
    c_low = float(data[i][4])
    c_close = float(data[i][5])

    candle_direction = fn.is_bull_candle(c_open, c_close) # 0-Bear, 1-Bull
    candle_range = fn.calculate_range(c_high, c_low)
    candle_high = fn.calculate_high(c_open, c_high, c_low, c_close)
    candle_body = fn.calculate_body(c_open, c_high, c_low, c_close)
    candle_low = fn.calculate_low(c_open, c_high, c_low, c_close)

    j = i+1
    c_open = float(data[j][2])
    c_close = float(data[j][5])
    next_candle_bull = fn.is_bull_candle(c_open, c_close) # 0-Bear, 1-Bull

    npdata = np.append(npdata, np.array([
        [candle_high],
        [candle_body],
        [candle_low],
        [candle_direction],
        [next_candle_bull]
    ]), axis=1)

    # print(candle_id)
    # print(j)
    i += 1


# print(npdata.shape)
# print(npdata)


