import functions as fn
import numpy as np

import csv
with open('import.csv', "r", newline='') as csv_file:
    data = list(csv.reader(csv_file))
csv_file.close()

# creating an empty 1d array of int type
npdata = np.empty((0, 12), int)   # 0,2 or 2d etc.

# using np.append() to add rows to array
i = 0
while i <= len(data)-3:
    c_open = float(data[i][2])
    c_high = float(data[i][3])
    c_low = float(data[i][4])
    c_close = float(data[i][5])

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
        [str(candle_high),
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
         str(next2_candle_bull)]
    ]), axis=0)

    # npdata = np.append(npdata, np.array([
    #     [str(candle_high),
    #     str(candle_body),
    #     str(candle_low),
    #     str(candle_bull),
    #     str(next_candle_bull)]
    # ]), axis=0)

    i += 2

with open('export.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(npdata)
