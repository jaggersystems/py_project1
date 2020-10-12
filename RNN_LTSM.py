import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

CSV_COLUMN_NAMES = ["Date", "Time", "Open", "High", "Low", "Close", "Volume"]
data = pd.read_csv("GBPUSDH4.csv", names=CSV_COLUMN_NAMES, date_parser=True)
data.pop("Time") # Remove Time Column

data_training = data[data["Date"]<"2019-01-01"].copy()
# print(data_training.tail())

data_test = data[data["Date"]>"2019-01-01"].copy()
# print(data_test)

training_data = data_training.drop(["Date"], axis=1)
# print(training_data.head())

# Scale the data between 0 and 1
scaler = MinMaxScaler()
training_data = scaler.fit_transform(training_data)
# print(training_data)

X_train = []
y_train = []

# print(training_data.shape[0])

for i in range(60, training_data.shape[0]):
    X_train.append(training_data[i-60:i])
    y_train.append(training_data[i, 0])

X_train, y_train = np.array(X_train), np.array((y_train))
# print(X_train.shape)
# print(y_train.shape)



#
# Build LSTM
#
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

# Create a callback that saves the model's weights
# Include the epoch in the file name (uses `str.format`)
checkpoint_path = "training_2/cp-{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights every 5 epochs
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    verbose=1,
    save_weights_only=True,
    period=5)

# Multi-GPU
strategy = tf.distribute.MirroredStrategy(cross_device_ops=tf.distribute.HierarchicalCopyAllReduce())
with strategy.scope():
    regressior = Sequential()

    regressior.add(LSTM(units=60, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 5)))
    regressior.add(Dropout(0.2))

    regressior.add(LSTM(units=60, activation='relu', return_sequences=True))
    regressior.add(Dropout(0.2))

    regressior.add(LSTM(units=80, activation='relu', return_sequences=True))
    regressior.add(Dropout(0.2))

    regressior.add(LSTM(units=120, activation='relu'))
    regressior.add(Dropout(0.2))

    regressior.add(Dense(units=2)) # 1 output

    regressior.compile(optimizer='Adam', loss='mean_squared_error')
    regressior.save_weights(checkpoint_path.format(epoch=0))
    regressior.fit(X_train, y_train, epochs=12, batch_size=128, callbacks=[cp_callback])  # Pass callback to training



# # load pre-trained data
# latest = tf.train.latest_checkpoint(checkpoint_dir)
# regressior.load_weights(latest)



#
# Prepare Test Dataset
#

past_60_days = data_training.tail(60)
df = past_60_days.append(data_test, ignore_index=True)
df = df.drop(["Date"], axis=1)

inputs = scaler.transform(df)
# print(inputs)

X_test = []
y_test = []

for i in range(60, inputs.shape[0]):
    X_test.append(inputs[i-60: i])
    y_test.append(inputs[i, 0])

X_test, y_test = np.array(X_test), np.array(y_test)

# print(X_test.shape)
# print(y_test.shape)

y_pred = regressior.predict(X_test)
# print(y_pred)

# scaler.scale_
# print(scaler.scale_)

scale = 1/1.09499042e+00
# print(scale)

y_pred = y_pred*scale
y_test = y_test*scale
# print(y_pred)
# print(y_test)



#
# Visualize Data
#

plt.figure(figsize=(14,5))
plt.plot(y_test, color = "red", label= "Real Price")
plt.plot(y_pred, color = "blue", label="Predicted Price")
plt.title("Price Prediction")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()


