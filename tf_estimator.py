import tensorflow as tf
import pandas as pd
import os
from tensorflow import estimator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Hides all un-nessesary logging


CSV_COLUMN_NAMES = ["High", "Body", "Low", "Candle", "Next_High", "Next_Body", "Next_Low", "Next_Candle"]
NEXT_CANDLE = ["1", "0"]

train = pd.read_csv("train.csv", names=CSV_COLUMN_NAMES, header=0)
test = pd.read_csv("test.csv", names=CSV_COLUMN_NAMES, header=0)

train_y = train.pop('Next_Candle')
test_y = test.pop('Next_Candle')


def input_fn(features, labels, training=True, batch_size=256):
    """An input function for training or evaluating"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle and repeat if you are in training mode.
    if training:
        dataset = dataset.shuffle(1000).repeat()

    return dataset.batch(batch_size)


# Feature columns describe how to use the input.
my_feature_columns = []
for key in train.keys():
    my_feature_columns.append(tf.feature_column.numeric_column(key=key))


# Build a DNN with 2 hidden layers with 30 and 10 hidden nodes each.
classifier = tf.estimator.DNNClassifier(
    feature_columns=my_feature_columns,
    # Two hidden layers of 30 and 10 nodes respectively.
    hidden_units=[30, 10],
    # The model must choose between 3 classes.
    n_classes=3)


# Train the Model.
classifier.train(
    input_fn=lambda: input_fn(train, train_y, training=True),
    steps=50000)


eval_result = classifier.evaluate(
    input_fn=lambda: input_fn(test, test_y, training=False))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

#
# def predict(x):
#     example = tf.train.Example()
#     example.features.feature["x"].float_list.value.extend([x])
#     return imported.signatures["predict"](
#         examples=tf.constant([example.SerializeToString()]))
#
#
# expected = ['1', '0']
# predict_x = {
#     'High': [25],
#     'Body': [75],
#     'Low': [0],
#     'Candle': [1],
# }

'''
20,50,30,1  10,35,55,1
10,35,55,1,75,10,15,1

05,85,10,0,25,75,00,1,1
25,75,00,1,05,25,70,0,0

55,05,40,0,35,15,50,1,1
35,15,50,1,50,45,05,0,0

10,85,05,0,20,80,00,1,1
20,80,00,1,10,55,35,0,0
'''