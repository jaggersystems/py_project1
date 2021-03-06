import numpy as np
import functions as fn

# Date[0], Time[1], Open[2], High[3], Low[4], Close[5], Volume[6]
import csv
with open('GBPUSDH4_small.csv', "r", newline='') as csv_file:
    data = list(csv.reader(csv_file))
csv_file.close()


# creating an empty 1d array of int type
npdata = np.empty((1, 0), int)   # 0,2 or 2d etc.

# using np.append() to add rows to array
i = 0
while i <= len(data)-2:
    c_open = float(data[i][2])
    c_high = float(data[i][3])
    c_low = float(data[i][4])
    c_close = float(data[i][5])

    candle_bull = fn.is_bull_candle(c_open, c_close) # 0-Bear, 1-Bull
    candle_range = fn.calculate_range(c_high, c_low)
    candle_high = str(format(fn.calculate_high(c_open, c_high, c_low, c_close), "02"))
    candle_body = str(format(fn.calculate_body(c_open, c_high, c_low, c_close), "02"))
    candle_low = str(format(fn.calculate_low(c_open, c_high, c_low, c_close), "02"))

    candle_id = candle_high + "" + candle_body + "" + candle_low

    j = i+1

    c_open = float(data[j][2])
    c_close = float(data[j][5])
    next_candle_bull = fn.is_bull_candle(c_open, c_close) # 0-Bear, 1-Bull

    npdata = np.append(npdata, np.array([
        # [str(candle_high)],
        # [str(candle_body)],
        # [str(candle_low)],
        [str(candle_id),
        str(candle_bull),
        next_candle_bull]
    ]), axis=1)

    i += 1

with open('export.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(npdata)

