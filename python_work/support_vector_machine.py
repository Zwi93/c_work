import pandas as pd 
import numpy as np
from random import choices
from sklearn import svm
import matplotlib.pyplot as plt
from math import sqrt, pow
from yahoo_data_prep import create_features

'''
iris_data = pd.read_csv("Iris.csv")
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
'''
'''
#fname = "index_data.xlsx"
#df = create_features(fname, "SP500")
fname = "currency_data.xlsx"
df = create_features(fname, "USDZAR")
df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
cols = ['ret_1', 'ret_2']
X_train = df.loc[:, cols]
y_classifier = df.return_sign

#Seperate points into up/down moves.
up_moves = df[df['return_sign'] == 1.0]
down_moves = df[df['return_sign'] == -1.0]
plt.scatter(up_moves['ret_1'], up_moves['ret_2'], color='g')
plt.scatter(down_moves['ret_1'], down_moves['ret_2'], color='r')

#clf = svm.LinearSVC(C=1) 
#clf = svm.SVC(kernel='linear', C=1000)
#clf.fit(X_train, y_classifier)

#X_test = np.array([0.2, 0.1]).reshape(1, -1)

#print(clf.predict(X_test))

#plt.show()
'''

class SVMClassifier (svm.SVC):
    def get_train_data (self, fname, asset_class, cols):
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
        X_train = df.loc[:, cols]
        y_classifier = df.return_sign

        return X_train, y_classifier

    def fit_test_model (self, fname, asset_class, cols):
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        self.fit(X_train, y_classifier)
        X_test = np.array([0.2, 0.1]).reshape(1, -1)

        return self.predict(X_test)

    def get_feature_scatter_plt (self, fname, asset_class, cols, ax):
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.

        #Seperate points into up/down moves.
        up_moves = df[df['return_sign'] == 1.0]
        down_moves = df[df['return_sign'] == -1.0]
        ax.scatter(up_moves['ret_1'], up_moves['ret_2'], color='g', s=1)
        ax.scatter(down_moves['ret_1'], down_moves['ret_2'], color='r', s=1)

    def svm_decision_boundary_plot (self, fname, asset_class, cols, ax):
        #Setup the axes environment parameters.
        #xlim = ax.get_xlim()
        xlim = (-0.1, 0.1)
        #ylim = ax.get_ylim()
        ylim = (-0.1, 0.1)
        x_grid = np.linspace(xlim[0], xlim[1], 30)
        y_grid = np.linspace(ylim[0], ylim[1], 30)
        Y, X = np.meshgrid(y_grid, x_grid)
        xy_grid = np.vstack([X.ravel(), Y.ravel()]).T

        #Train the model on data and give out the decision boundary.
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        self.fit(X_train, y_classifier)
        decision_boundary = self.decision_function(xy_grid).reshape(X.shape)

        #Plot the decision boundary for a given C.
        ax.contour(X, Y, decision_boundary, colors='k', alpha=0.5, linestyles=['--', '-', '--'])

        #plot the support vectors for the determined model.
        margin_vectors = self.support_vectors_
        ax.scatter(margin_vectors[:, 0], margin_vectors[:, 1], s=20, facecolors='none', color='orange')




#fname = "currency_data.xlsx"
fname = "index_data.xlsx"
cols = ['ret_1', 'ret_2']
#asset_class = 'USDZAR'
asset_class = 'SP500'
ax = plt.gca()

#Create SVM object.
svm_object = SVMClassifier(C=1e5, kernel='linear')
#svm_predict = svm_object.fit_test_model(fname, asset_class, cols)
#print(svm_predict)
svm_object.svm_decision_boundary_plot(fname, asset_class, cols, ax)
svm_object.get_feature_scatter_plt(fname, asset_class, cols, ax)

plt.show()