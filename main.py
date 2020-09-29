# Date[0], Close[1], Open[2], High[3], Low[4], Change %[5]

import numpy as np
import csv

with open('EURUSD.csv', "r", newline='') as csvfile:
    data = list(csv.reader(csvfile))
csvfile.close()

# def calculate_c_percent(close, open, high, low):


# print(data[1][1])

c_close = float(data[1][1])
c_open = float(data[1][2])
c_high = float(data[1][3])
c_low = float(data[1][4])


c_range = c_high - c_low

c_high_percent = ((c_high - c_open)/c_range) * 100
c_body_percent = ((c_open - c_close)/c_range) * 100
c_low_percent = 100 - c_high_percent - c_body_percent

green_candle = True

if (c_open < c_close):
    green_candle = True
    c_price_movement = round((c_close - c_open), 4)
else:
    green_candle = False
    c_price_movement = round((c_open - c_close), 4)



print("\nHigh%: " + str(c_high_percent))
print("Body%: " + str(c_body_percent))
print("Low%: " + str(c_low_percent))

print("The Open is: " + str(c_open))
print("The Close is: " + str(c_close))
print("Pips: " + str(c_price_movement))
