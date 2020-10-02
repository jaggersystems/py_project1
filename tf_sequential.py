import numpy as np
import functions as fn

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler

# Date[0], Time[1], Open[2], High[3], Low[4], Close[5], Volume[6]
import csv
with open('GBPUSDH4.csv', "r", newline='') as csv_file:
    data = list(csv.reader(csv_file))
csv_file.close()

train_samples = []
train_labels = []


# creating an empty 1d array of int type
# npdata = np.empty((5,0), int)   # 0,2 or 2d etc.

# using np.append() to add rows to array
i = 0
while i <= len(data)-2:
    c_open = float(data[i][2])
    c_high = float(data[i][3])
    c_low = float(data[i][4])
    c_close = float(data[i][5])

    candle_direction = fn.is_bull_candle(c_open, c_close) # 0-Bear, 1-Bull
    candle_range = fn.calculate_range(c_high, c_low)
    candle_high = str(format(fn.calculate_high(c_open, c_high, c_low, c_close), "02"))
    candle_body = str(format(fn.calculate_body(c_open, c_high, c_low, c_close), "02"))
    candle_low = str(format(fn.calculate_low(c_open, c_high, c_low, c_close), "02"))

    candle_id = candle_high + "" + candle_body + "" + candle_low

    # train_samples.append(candle_high)
    train_samples.append(candle_id)

    j = i+1
    c_open = float(data[j][2])
    c_close = float(data[j][5])
    next_candle_direction = fn.is_bull_candle(c_open, c_close) # 0-Bear, 1-Bull

    train_labels.append(next_candle_direction)

    # npdata = np.append(npdata, np.array([
    #     [str(candle_high)],
    #     [str(candle_body)],
    #     [str(candle_low)],
    #     [str(candle_direction)],
    #     [next_candle_direction],
    # ]), axis=1)

    # print(candle_id)
    # print(j)
    i += 1

'''
['21' '21' '04' '23' '23']
[1 1 0 0 0]
'''
# for i in train_sample_high:
#     print(i)

train_samples = np.array(train_samples)
train_labels = np.array(train_labels)

# Shuffle direction before passing to model.
# Doing this ensures data is shuffled to be used in model.fit(validation_split=0.1...) as validation
# data generated is not shuffled automatically.
train_samples, train_labels = shuffle(train_samples, train_labels)

# print(train_samples)
# print(train_labels)


# Scale the data in to a usable sample range classifying each entry between 0 and 1
scaler = MinMaxScaler(feature_range=(0,1))
scaled_train_samples = scaler.fit_transform(train_samples.reshape(-1, 1))

# for i in scaled_train_samples:
#     print(i)

physical_devices = tf.config.experimental.list_physical_devices('GPU')
print("Num GPUs Available: ", len(physical_devices))
tf.config.experimental.set_memory_growth(physical_devices[0], True)

model = Sequential([
    Dense(units=16, input_shape=(1,), activation='relu'),
    Dense(units=32, activation='relu'),
    Dense(units=2, activation='softmax')
])

# model.summary()

model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy']
)

model.fit(x=scaled_train_samples,
          y=train_labels, validation_split=0.1,
          batch_size=10,
          epochs=30,
          shuffle=True,
          verbose=2
          )