import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Hides all un-nessesary logging

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Initialization of Tensors
x = tf.constant(5, shape=(1, 1), dtype=tf.float32)
x = tf.constant([[1,2,3], [4,5,6]])

x = tf.ones((3,3))
x = tf.zeros((2,3))
x = tf.eye(3) # I for the indentity matrix in linear algebra
x = tf.random.normal((3,3), mean=0, stddev=1)
x = tf.random.uniform((1,3), minval=0, maxval=1)
x = tf.range(start=1, limit=10, delta=2)
x = tf.cast(x, dtype=tf.float64)  # tf.float, tf.int, tf.bool


# Mathematical operations

x = tf.constant([1,2,3])
y = tf.constant([9,8,7])
z = tf.add(x, y)
z = x + y # same as above

z = tf.subtract(x, y)
z = x - y

z = tf.divide(x, y)
z = x / y

z = tf.multiply(x, y)
z = x * y

z = tf.tensordot(x, y, axes=1)
z = tf.reduce_sum(x * y, axis=0)

z = x ** 5

x = tf.random.normal((2, 3))
y = tf.random.normal((3, 4))
z = tf.matmul(x, y)
z = x @ y
# print(z)


# Indexing
x = tf.constant([0, 1, 1, 2, 3, 1, 2, 3])
# print(x[::2]) # every other index
# print(x[::-1]) # reverse order

indices = tf.constant([0, 3])
x_ind = tf.gather(x, indices)
# print(x_ind)

x = tf.constant([[1, 2],
                [3, 4],
                [5, 6]])
# print(x[0])
# print(x[0,:])
# print(x[0:2,:])


# Reshaping
x = tf.range(9)
# print(x)

x = tf.reshape(x, (3,3))
# print(x)

x = tf.transpose(x, perm=[1, 0])
# print(x)


# import data
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# flatten data from 2 columns to 1 columns
x_train = x_train.reshape(-1, 28*28).astype("float32") /  255.0
x_test = x_test.reshape(-1, 28*28).astype("float32") / 255.0

model = keras.Sequential(
    [
        keras.Input(shape=(28, 28)),
        layers.Dense(512, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(10),
     ]
)

model = keras.Sequential()
model.add(keras.Input(shape=(784)))
model.add(layers.Dense(512, activation='relu'))
print(model.summary()) # for debugging
model.add(layers.Dense(256, activation='relu', name='my_layer'))
model.add(layers.Dense(10))
model = keras.Model(inputs=model.inputs,
                    outputs=[model.layers[-2].output])

feature = model.predict(x_train)
print(feature.shape)
#
# import sys
# sys.exit()

# Functional API
inputs = keras.Input(shape=(784))
x = layers.Dense(512, activation='relu', name='first_layer')(inputs)
x = layers.Dense(256, activation='relu', name='second_layer')(x)
outputs = layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs=inputs, outputs=outputs)
print(model.summary())

# import sys
# sys.exit()

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer=keras.optimizers.Adam(lr=0.001),
    metrics=["accuracy"],
)

model.fit(x_train, y_train, batch_size=32, epochs=5, verbose=2)
model.evaluate(x_test, y_test, batch_size=32, verbose=2)