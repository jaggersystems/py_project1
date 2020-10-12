import functions as fn
import numpy as np
import glob
import os
import pandas as pd
import csv

path = r'C:\Users\Stefan\PycharmProjects\py_project1\data-big\H1'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

col_names = ["Date", "Time", "Open", "High", "Low", "Close", "Volume"]
df_from_each_file = (pd.read_csv(f, header=None, names=col_names) for f in all_files)
pd_data = pd.concat(df_from_each_file, ignore_index=True)

# Displays numbers from dataframe without e+05 type numbers
pd.options.display.float_format = '{:,.4f}'.format  # set other global format




# print(pd_data.describe())

# remove row if not much volume
pd_data = pd_data.drop(pd_data[pd_data.Volume < 1000].index)

# Remove : and 0 from Time column
pd_data['Time'] = pd_data['Time'].str.replace(':00', '', regex=False)
pd_data['Time'] = pd_data['Time'].str.replace('00', '99', regex=False)

# print(pd_data.tail())
# print(pd_data.describe())



# convert our pandas data to numpy array
data = pd_data.to_numpy()

# creating an empty 1d array of int type
npdata = np.empty((0, 14), int)

# ["Date", "Time", "Open", "High", "Low", "Close", "Volume"]

# using np.append() to add rows to array
i = 0
while i <= len(data)-3:
    c_open = float(data[i][2])
    c_high = float(data[i][3])
    c_low = float(data[i][4])
    c_close = float(data[i][5])
    c_volume = int(data[i][6])
    c_time = str(data[i][1])

    candle_bull = fn.is_bull_candle(c_open, c_close) # 0-Bear, 1-Bull
    candle_range = fn.calculate_range(c_high, c_low)
    candle_high = str(format(fn.calculate_high(c_open, c_high, c_low, c_close), "02"))
    candle_body = str(format(fn.calculate_body(c_open, c_high, c_low, c_close), "02"))
    candle_low = str(format(fn.calculate_low(c_open, c_high, c_low, c_close), "02"))

    j = i+1
    c_open = float(data[j][2])
    c_high = float(data[j][3])
    c_low = float(data[j][4])
    c_close = float(data[j][5])

    next_candle_bull = fn.is_bull_candle(c_open, c_close)  # 0-Bear, 1-Bull
    next_candle_range = fn.calculate_range(c_high, c_low)
    next_candle_high = str(format(fn.calculate_high(c_open, c_high, c_low, c_close), "02"))
    next_candle_body = str(format(fn.calculate_body(c_open, c_high, c_low, c_close), "02"))
    next_candle_low = str(format(fn.calculate_low(c_open, c_high, c_low, c_close), "02"))

    k = j+1
    c_open = float(data[k][2])
    c_high = float(data[k][3])
    c_low = float(data[k][4])
    c_close = float(data[k][5])

    next2_candle_bull = fn.is_bull_candle(c_open, c_close)  # 0-Bear, 1-Bull
    next2_candle_range = fn.calculate_range(c_high, c_low)
    next2_candle_high = str(format(fn.calculate_high(c_open, c_high, c_low, c_close), "02"))
    next2_candle_body = str(format(fn.calculate_body(c_open, c_high, c_low, c_close), "02"))
    next2_candle_low = str(format(fn.calculate_low(c_open, c_high, c_low, c_close), "02"))

    npdata = np.append(npdata, np.array([
        [
        str(c_time),
        str(candle_high),
        str(candle_body),
        str(candle_low),
        str(candle_bull),
        str(next_candle_high),
        str(next_candle_body),
        str(next_candle_low),
        str(next_candle_bull),
        str(next2_candle_high),
        str(next2_candle_body),
        str(next2_candle_low),
        str(next2_candle_bull),
        str(c_volume)]
    ]), axis=0)

    i += 3

with open('export.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(npdata)
