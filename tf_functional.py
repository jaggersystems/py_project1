import numpy as np
import pandas as pd

import tensorflow as tf

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split


import pathlib

CSV_COLUMN_NAMES = ["High", "Body", "Low", "Candle", "Next_High", "Next_Body", "Next_Low",
                    "Next_Candle", "Next2_High", "Next2_Body", "Next2_Low", "Next2_Candle"]
dataframe = pd.read_csv("export.csv", names=CSV_COLUMN_NAMES, header=0)

# print(dataframe.head())

train, test = train_test_split(dataframe, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)
# print(len(train), 'train examples')
# print(len(val), 'validation examples')
# print(len(test), 'test examples')


# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('Next2_Candle')
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  return ds


batch_size = 5 # A small batch sized is used for demonstration purposes
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

# for feature_batch, label_batch in train_ds.take(1):
#   print('Every feature:', list(feature_batch.keys()))
#   print('A batch of ages:', feature_batch['High'])
#   print('A batch of targets:', label_batch )


# We will use this batch to demonstrate several types of feature columns
test_batch = next(iter(train_ds))[0]

# A utility method to create a feature column and to transform a batch of data
def create_feature_column(feature_column):
  feature_layer = layers.DenseFeatures(feature_column)
  # print(feature_layer(test_batch).numpy())


feature_columns = []

for header in ["High", "Body", "Low", "Candle", "Next_High", "Next_Body", "Next_Low",
               "Next_Candle", "Next2_High", "Next2_Body", "Next2_Low"]:
    feature_columns.append(feature_column.numeric_column(header))

breed1 = feature_column.categorical_column_with_vocabulary_list(
      'Breed1', dataframe.Breed1.unique())
breed1_embedding = feature_column.embedding_column(breed1, dimension=8)
create_feature_column(breed1_embedding)


feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

batch_size = 32
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)


model = tf.keras.Sequential([
  feature_layer,
  layers.Dense(128, activation='relu'),
  layers.Dense(128, activation='relu'),
  layers.Dropout(.1),
  layers.Dense(1)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_ds,
          validation_data=val_ds,
          epochs=15)

loss, accuracy = model.evaluate(test_ds)
print("Accuracy", accuracy)


