import pandas as pd 
import numpy as np
from random import choices
from sklearn import svm
import matplotlib.pyplot as plt
from math import sqrt, pow

iris_data = pd.read_csv("Iris.csv")
fig = plt.figure(figsize=(10, 6))

#Sort out data to split unwanted categories.
iris_data_np = np.array(iris_data)
iris_data_np[iris_data_np == 'Iris-setosa'] = 1
iris_data_np[iris_data_np == 'Iris-virginica'] = 0

colms = np.array([1, 2, 5])
setosa_condition = np.where(iris_data_np[:, -1:] == 1)
setosa_iris_data = iris_data_np[setosa_condition[0][:, None], colms]

versicolor_condition = np.where(iris_data_np[:, -1:] == 0)
versicolor_iris_data = iris_data_np[versicolor_condition[0][:, None], colms]

plt.scatter(setosa_iris_data[:, 0], setosa_iris_data[:, 1], color = 'b')
plt.scatter(versicolor_iris_data[:, 0], versicolor_iris_data[:, 1], color = 'g')

sliced_iris_data = np.concatenate((setosa_iris_data, versicolor_iris_data), axis=0)

y_id = sliced_iris_data[:, 2].astype('int')
X_train = sliced_iris_data[:, : 2]

clf = svm.LinearSVC() 
#clf = svm.SVC(kernel='linear', C=1000)
clf.fit(X_train, y_id)

X_test = np.array([2.2, 4.1]).reshape(1, -1)
clf.predict(X_test)

plt.show()
