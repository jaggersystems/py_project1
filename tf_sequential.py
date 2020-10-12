import numpy as np
import functions as fn

import pandas as pd

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler


# CSV_COLUMN_NAMES = ["High", "Body", "Low", "Candle", "Next_Candle"]
CSV_COLUMN_NAMES = ["High", "Body", "Low", "Candle" "Next_High", "Next_Body", "Next_Low", "Next_Candle", "Next2_High", "Next2_Body", "Next2_Low", "Next2_Candle"]
NEXT_CANDLE = ["1", "0"]

train = pd.read_csv("export.csv", names=CSV_COLUMN_NAMES, header=0)
# test = pd.read_csv("test.csv", names=CSV_COLUMN_NAMES, header=0)


train_y = train.pop('Next2_Candle')


train_samples = np.array(train)
train_labels = np.array(train_y)

# Shuffle direction before passing to model.
# Doing this ensures data is shuffled to be used in model.fit(validation_split=0.1...) as validation
# data generated is not shuffled automatically.

# train_samples, train_labels = shuffle(train_samples, train_labels)
#
# print(train_samples)
# print(train_labels)

#
# # Scale the data in to a usable sample range classifying each entry between 0 and 1
# scaler = MinMaxScaler(feature_range=(0, 1))
# scaled_train_samples = scaler.fit_transform(train_samples)
#
# # print(scaled_train_samples)
#
#
# # physical_devices = tf.config.experimental.list_physical_devices('GPU')
# # print("Num GPUs Available: ", len(physical_devices))
# # tf.config.experimental.set_memory_growth(physical_devices[0], True)
#
# model = Sequential([
#     Dense(units=64, input_shape=(10,), activation='relu'),
#     Dense(units=64, activation='relu'),
#     Dense(units=10, activation='softmax')
# ])
#
# model.compile(optimizer=Adam(learning_rate=0.0001),
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy']
# )
#
# model.fit(x=train_samples,
#           y=train_labels, validation_split=0.2,
#           batch_size=10,
#           epochs=30,
#           shuffle=True,
#           verbose=2
#           )