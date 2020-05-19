import pandas as pd 
import numpy as np
from random import choices
from sklearn import svm
import matplotlib.pyplot as plt
from math import sqrt, pow
from yahoo_data_prep import create_features, get_colums_names
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit, KFold, GridSearchCV

#Function to compute powerset of a list.
def powerset(s):
    x = len(s)
    power_set = []
    for i in range(1 << x):
        subset = [s[j] for j in range(x) if (i & (1 << j))]
        power_set.append(subset)

    return power_set 


class SVMClassifier (svm.SVC):
    def get_train_data (self, fname, asset_class, cols):
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
        X_train = df.loc[:, cols]
        y_classifier = df.return_sign

        return X_train, y_classifier

    def scaling_function (self, fname, asset_class, cols):
        scaler = StandardScaler()
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        #Scale the training data. Also, test data must be scaled.
        scaled_df = scaler.fit_transform(X_train)

        return scaled_df, y_classifier

    def fit_test_model (self, fname, asset_class, cols):
        #Data is scaled 1st. Next change the dataframe to a numpy array.
        X_train = self.scaling_function(fname, asset_class, cols)[0]
        y_classifier = self.scaling_function(fname, asset_class, cols)[1]
        self.fit(X_train, y_classifier)
        X_test = np.array([0.2, 0.1]).reshape(1, -1)

        return self.dual_coef_, self.n_support_

    def get_feature_scatter_plt (self, fname, asset_class, cols, ax):
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.

        #Seperate points into up/down moves.
        up_moves = df[df['return_sign'] == 1.0]
        down_moves = df[df['return_sign'] == -1.0]
        ax.scatter(up_moves[cols[0]], up_moves[cols[1]], color='g', s=1)
        ax.scatter(down_moves[cols[0]], down_moves[cols[1]], color='r', s=1)

    def svm_decision_boundary_plot (self, fname, asset_class, cols, ax):
        #Setup the axes environment parameters.
        #xlim = ax.get_xlim()
        xlim = (-0.1, 0.1)
        #ylim = ax.get_ylim()
        ylim = (-10, 10)
        x_grid = np.linspace(xlim[0], xlim[1], 5)
        y_grid = np.linspace(ylim[0], ylim[1], 5)
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

    def scoring_selection_gridCV (self, fname, asset_class, cols, ax):
        #Perform scoring and selection of best estimator from a range of parameters. Try different combinations of clomns.
        params_grid = {'C': [0.01, 0.02, 0.05, 0.1, 0.2]}
        cv_1 = KFold(n_splits=3, shuffle=False, random_state=1)
        cv_2 = KFold(n_splits=3, shuffle=False, random_state=1)
        #cols_subsets = [cols, cols[:3], cols[3:], cols[-3:], cols[:-3]]
        cols_subsets = powerset(cols)[1:]
        #Create dictionary for storing scores.
        scores_array = {}
        index = 0

        for cols in cols_subsets:
            #Create object of GridSearchCV to use for scoring. 
            clf = GridSearchCV(estimator = self, param_grid=params_grid, cv = cv_1)
            X, y = self.get_train_data(fname, asset_class, cols)
            nested_score = cross_val_score(clf, X=X, y=y, cv=cv_2)
            index += 1
            scores_array[index] = nested_score.mean()

        x = list(scores_array.keys()); y = scores_array.values()

        ax.scatter(x, y)

#fname = "currency_data.xlsx"
fname = "index_data.xlsx"
cols = ['ret_1', 'momentum_1d']
#asset_class = 'USDZAR'
asset_class = 'VIX'
all_cols = get_colums_names(fname, asset_class)
ax = plt.gca()

#Create SVM object.
svm_object = SVMClassifier(C=0.01, kernel='linear', cache_size = 1000)
#svm_predict = svm_object.fit_test_model(fname, asset_class, cols)
#print(svm_predict)
#svm_object.svm_decision_boundary_plot(fname, asset_class, cols, ax)
#svm_object.get_feature_scatter_plt(fname, asset_class, cols, ax)
svm_object.scoring_selection_gridCV(fname, asset_class, all_cols, ax)
plt.show()