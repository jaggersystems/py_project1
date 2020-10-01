import numpy as np

# Date[0], Time[1], Open[2], High[3], Low[4], Close[5], Volume[6]
import csv
with open('EURUSD.csv', "r", newline='') as csv_file:
    data = list(csv.reader(csv_file))
csv_file.close()

# data = [[25,9,1.16677,1.16843,1.16114,1.16303,726665], [26,9,1.16245,1.16793,1.16144,1.16654,720030], [27,9,1.16654,1.17447,1.16608,1.17414,700881]]


def is_bull_candle(f_open, f_close):
    if f_close > f_open:
        return 1
    else:
        return 0


def calculate_range(f_high, f_low):
    f_true_range = (f_high - f_low)
    # c_pips = int(c_true_range * 10000)  # TODO: Return pips
    return f_true_range


def calculate_high(f_open, f_high, f_low, f_close):
    if is_bull_candle(f_open, f_close):
        # print("bull")
        f_high_percent = ((f_high - f_close) / calculate_range(f_high, f_low)) * 100
    else:
        # print("bear")
        f_high_percent = ((f_high - f_open) / calculate_range(f_high, f_low)) * 100
    return round(f_high_percent)


def calculate_body(f_open, f_high, f_low, f_close):
    if is_bull_candle(f_open, f_close):
        f_body_percent = ((f_close - f_open) / calculate_range(f_high, f_low)) * 100
    else:
        f_body_percent = ((f_open - f_close) / calculate_range(f_high, f_low)) * 100
    return round(f_body_percent)


def calculate_low(f_open, f_high, f_low, f_close):
    f_low_percent = 100 - calculate_high(f_open, f_high, f_low, f_close) - calculate_body(f_open, f_high, f_low, f_close)
    return round(f_low_percent)


def round_number(num_input, base=5):
    # base = 5 rounds the number to this nearest value, so 25, 30, 35 etc.
    return base * round(float(num_input) / base)


i = 2
# 0 = bear = S-22.77-51.3-25.93-72
# 1 = bull = L-21.42-63.02-15.56-64

c_open = float(data[i][2])
c_high = float(data[i][3])
c_low = float(data[i][4])
c_close = float(data[i][5])

candle_bull = is_bull_candle(c_open, c_close)
candle_range = calculate_range(c_high, c_low)
candle_high = calculate_high(c_open, c_high, c_low, c_close)
candle_body = calculate_body(c_open, c_high, c_low, c_close)
candle_low = calculate_low(c_open, c_high, c_low, c_close)

# print("is_bull_candle: " + str(candle_bull))
# print("calculate_range: " + str(candle_range))
# print("calculate_high: " + str(candle_high))
# print("calculate_body: " + str(candle_body))
# print("calculate_low: " + str(candle_low) + "\n")

candle_id = str(round_number(candle_high)) + "_" + str(round_number(candle_body)) + "_" + str(round_number(candle_low))
print(candle_id)


#
# # creating an empty 2d array of int type
# nparray = np.empty((0,2), int)
# print("Empty array:")
# print(nparray)
#
# # adding two new rows to empt_array
# # using np.append()
# nparray = np.append(nparray, np.array([[10, 20]]), axis=0)
# nparray = np.append(nparray, np.array([[40, 50]]), axis=0)
#
# print("\nNow array is:")
# print(nparray)


# i = 0
# while i <= len(data)-1:
#     c_open = float(data[i][2])
#     c_high = float(data[i][3])
#     c_low = float(data[i][4])
#     c_close = float(data[i][5])
#
#     a = np.array(build_candle_id(c_close, c_open, c_high, c_low))
#     # print(a)
#     i += 1


