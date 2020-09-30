# Date[0], Time[1], Open[2], High[3], Low[4], Close[5], Volume[6]

from ahocorapy.keywordtree import KeywordTree
# from ahocorapy_visualizer.visualizer import Visualizer
# import pygraphviz as pgv

# import csv
# with open('EURUSD.csv', "r", newline='') as csv_file:
#     data = list(csv.reader(csv_file))
# csv_file.close()

data = [[25,9,1.16677,1.16843,1.16114,1.16303,726665], [26,9,1.16245,1.16793,1.16144,1.16654,720030], [27,9,1.16654,1.17447,1.16608,1.17414,700881]]


def build_candle_id(close, open, high, low):
    # print("Function Test:" + str(open) + "\n")
    c_true_range = (high - low)
    c_pips = int(c_true_range * 10000) # TODO: This is a hack fix to get to our 72 pips.

    if close > open:
        # we have a bull candle
        candle_direction = "L"
        c_high_percent = ((high - close) / c_true_range) * 100
        c_body_percent = ((close - open) / c_true_range) * 100
        c_low_percent = 100 - c_high_percent - c_body_percent
    else:
        # we have a bear candle
        candle_direction = "S"
        c_high_percent = ((high - open) / c_true_range) * 100
        c_body_percent = ((open - close) / c_true_range) * 100
        c_low_percent = 100 - c_high_percent - c_body_percent

    candle_id = candle_direction + "-" + str(round(c_high_percent, 2)) + "-" + str(round(c_body_percent, 2)) + "-" + str(round(c_low_percent, 2)) + "-" + str(c_pips)
    return candle_id

# 0 = bear
# 1 or 2 = bull
day_selector = 1

c_open = float(data[day_selector][2])
c_high = float(data[day_selector][3])
c_low = float(data[day_selector][4])
c_close = float(data[day_selector][5])

# print("Open Ref: " + str(c_open) + "\n")
# print(build_candle_id(c_close, c_open, c_high, c_low))

kwtree = KeywordTree(case_insensitive=True)
for index in range(len(data)):
    c_open = float(data[index][2])
    c_high = float(data[index][3])
    c_low = float(data[index][4])
    c_close = float(data[index][5])
    kwtree.add(build_candle_id(c_close, c_open, c_high, c_low))
kwtree.finalize()

results = kwtree.search_all('L-21.42-63.02-15.56-64')
for result in results:
    print(result)


# visualizer = Visualizer()
# visualizer.draw('readme_example.png', kwtree)