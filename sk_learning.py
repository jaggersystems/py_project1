import sklearn as sk
from sklearn import tree
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


col_names = ["Time", "High", "Body", "Low", "Candle", "Next_High", "Next_Body", "Next_Low", "Next_Candle",
             "Next2_High", "Next2_Body", "Next2_Low", "Next2_Candle", "Volume"]
data = pd.read_csv("export.csv", names=col_names)
feature_cols = ["Time", "High", "Body", "Low", "Candle", "Next_High", "Next_Body", "Next_Low", "Next_Candle"]

labels = ["Next2_Candle"]
X = data[feature_cols]
y = data[labels]



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)


# from sklearn.neighbors import KNeighborsClassifier
# clf = KNeighborsClassifier()

clf = tree.DecisionTreeClassifier()
clf = DecisionTreeClassifier(criterion = 'entropy', min_samples_split=1000)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

# print(X_test.head())

from sklearn.metrics import accuracy_score
print('Accuracy Score on train data: ', accuracy_score(y_true=y_train, y_pred=clf.predict(X_train)))
print('Accuracy Score on test data: ', accuracy_score(y_true=y_test, y_pred=y_pred))


print(clf.predict([[10,20,60,20,1,5,80,15,1]]))

# import os
# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin/'
# from graphviz import Source
#
# graph = Source( tree.export_graphviz(clf, out_file=None, feature_names=feature_cols))
# png_bytes = graph.pipe(format='png')
# with open('dtree_pipe.png','wb') as f:
#     f.write(png_bytes)
#
# from IPython.display import Image
# Image(png_bytes)


