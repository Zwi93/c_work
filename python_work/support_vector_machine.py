import pandas as pd 
import numpy as np
from random import choices
from sklearn import svm
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from math import sqrt, pow
from yahoo_data_prep import create_features, get_colums_names, get_dates
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit, KFold, GridSearchCV, cross_validate
from sklearn.metrics import confusion_matrix
register_matplotlib_converters()

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
        """Function to obtain training data (or training + test) from a dataframe.
        fname : name of the file under which the data is stored in the system's path.
        asset_class : name of the financial instrument to consider as contained in the file given by fname.
        """
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
        X_train = df.loc[:, cols]
        y_classifier = df.return_sign

        return X_train, y_classifier

    def scaling_function (self, fname, asset_class, cols):
        """Function to scale the features of vectors in the training (and test) data.
        """
        scaler = StandardScaler()
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        #Scale the training data. Also, test data must be scaled.
        scaled_df = scaler.fit_transform(X_train)

        return scaled_df, y_classifier

    def fit_test_model (self, fname, asset_class, cols):
        """Functionn to fit model and then test it, using the n_support_ parameter.
        """
        #Data is scaled 1st. Next change the dataframe to a numpy array.
        X_train = self.scaling_function(fname, asset_class, cols)[0]
        y_classifier = self.scaling_function(fname, asset_class, cols)[1]
        self.fit(X_train, y_classifier)

        return self.n_support_

    def fit_test_model0 (self, fname, asset_class, cols):
        """Functionn to fit model and then test it, without returning the no of support vectors.
        """
        #Data is scaled 1st. Next change the dataframe to a numpy array.
        X_train = self.scaling_function(fname, asset_class, cols)[0]
        y_classifier = self.scaling_function(fname, asset_class, cols)[1]
        self.fit(X_train, y_classifier)

    def fit_test_CV (self, fname, asset_class, cols):
        """Function to perform cross_validation to yield best output for any metric.
        """
        X, y = self.get_train_data(fname, asset_class, cols)
        validated_model = cross_validate(self, X, y, cv=5, return_estimator=True)  # This is a dictionary object.
    
        return validated_model

    def cross_validation_test (self, fname, asset_class, cols, ax):
        """Use cross validation to determine the precision on confusion matrix
        """
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        
        self.fit_test_model0(fname, asset_class, cols)
        unvalidated_classified_data = self.predict(X_train)
        matrix = confusion_matrix(y_classifier, unvalidated_classified_data)
        print('Confusion Matrix: ')
        print(matrix)
        
        #ax.scatter(X_train[cols[0]], unvalidated_classified_data , color='b', s=20)

        validated_model = self.fit_test_CV(fname, asset_class, cols)
        best_models = validated_model['estimator']
        best_scores = validated_model['test_score']
        max_score = max(best_scores)

        for score, model in zip(best_scores, best_models):
            if score == max_score:
                classified_test_data = model.predict(X_train)
                matrix = confusion_matrix(y_classifier, classified_test_data)
                print('Confusion Matrix VC: ')
                print(matrix)
            else:
                pass

        x_data1 = X_train[cols[0]]
        x_data2 = X_train[cols[0]]

        #To be able to plot test data must be 2d, higher dimensions impossible to plot.
        #ax.scatter(x_data1, classified_test_data, color='r', s=10)
        #ax.scatter(x_data2, y_classifier, color='orange')

    def get_feature_scatter_plt (self, fname, asset_class, cols, ax):
        """Function to plot a simple scatter for two features of the data set, while separating up/down movements.
        """
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.

        #Seperate points into up/down moves.
        up_moves = df[df['return_sign'] == 1.0]
        down_moves = df[df['return_sign'] == -1.0]
        ax.scatter(up_moves[cols[0]], up_moves[cols[1]], color='g', s=1, alpha=1, label='Up')
        ax.scatter(down_moves[cols[0]], down_moves[cols[1]], color='r', s=1, alpha=1, label='Down')
        ax.legend(fontsize=10)
        ax.set_title('2D Representation for 2 Features')
        ax.set_xlabel(cols[0])
        ax.set_ylabel(cols[1])

    def svm_decision_boundary_plot (self, fname, asset_class, cols, ax):
        """Function to represent support vectors and associated margin lines for 2 features.
        """
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
        ax.scatter(margin_vectors[:, 0], margin_vectors[:, 1], s=25, facecolors='none', color='black', alpha=10)

    def hard_vs_soft_margin (self, fname, asset_class, cols):
        """Function to examine the impact of softening the C parameter on the list of support vectors
        """
        c_params = [0.01, 0.02, 0.03]
        #c_params = [10, 20, 30, 40, 50]
        n_up_support_v = []
        n_down_support_v = []
        for c in c_params:
            self.C = c
            n_down = self.fit_test_model(fname, asset_class, cols)[0]
            n_up = self.fit_test_model(fname, asset_class, cols)[1]
            n_down_support_v.append(n_down)
            n_up_support_v.append(n_up)

        df = pd.DataFrame({'C Parameter':c_params, 'Up Support vectors': n_up_support_v, 'Down Support vectors':n_down_support_v})
        print(df)

    def scoring_selection_gridCV (self, fname, asset_class, cols, ax):
        """Perform scoring and selection of best estimator from a range of parameters. Try different combinations of colmns.
        """
        params_grid = {'C': [0.01, 0.02, 0.05, 0.1, 0.2]}
        cv_1 = KFold(n_splits=3, shuffle=False, random_state=1)
        cv_2 = KFold(n_splits=3, shuffle=False, random_state=1)
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

    def pnl_backtesting (self, fname, asset_class, cols):
        """Perform PnL backtesting to check how accurate is the PnL predicted by the model is given previous realised price returns.
        """
        X, y = self.get_train_data(fname, asset_class, cols)

        #Split the data into test and training data and train the model on the training data.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
        self.probability = True
        self.fit(X_train, y_train)
        probability_down = self.predict_proba(X_test)[:, 0]
        probability_up = self.predict_proba(X_test)[:, 1]
        predicted_direction = self.predict(X_test)
        xdata = get_dates(fname, asset_class)
        df0 = create_features(fname, asset_class)
        df0 = df0[df0['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification. And select the returns corresponding to the dates on the test data.
        df0 = df0[-X_test.shape[0]:]
        true_realised_return = df0['return']
        kelly_optimal_fraction = abs(probability_up - probability_down)
        realised_daily_profit = np.multiply(np.multiply(true_realised_return, predicted_direction), kelly_optimal_fraction)

        df = pd.DataFrame({'Prob-Down':probability_down, 'Prob-Up':probability_up, 'Predicted-Move':predicted_direction, 'Real-Move':y_test, 'Daily PnL':realised_daily_profit})
        #print(df.head(30))

        #Plot scatter plots for probabilities.
        #color_code = np.multiply(predicted_direction, y)   # 1 if probability UP was correct
        #cmap = ListedColormap(['r', 'g'])  # Red means incorrect prediction.
        #ax.scatter(xdata, probability_up, c=color_code, cmap=cmap)
        #ax.scatter(xdata, probability_down, c=color_code, cmap=cmap)
        #ax.set_title('Transition Probabilities for Down Moves')
        #ax.set_xlabel('Dates')
        #ax.set_ylabel('Probability')
        
        return df


#Setup model parameters.
#fname = "currency_data.xlsx"
fname = "index_data.xlsx"
asset_class = 'SP500'
all_cols = get_colums_names(fname, asset_class)

#Determine which combination of features to investigate; select one from all the possible combinations in the powerset.
feature_combination = powerset(all_cols)[205]
#ax = plt.gca()

#Create SVM object.
svm_object = SVMClassifier(C=0.01, kernel='linear', cache_size = 1000)
#svm_predict = svm_object.fit_test_model(fname, asset_class, cols)
#print(svm_predict)
#svm_object.svm_decision_boundary_plot(fname, asset_class, two_features, ax)
#svm_object.get_feature_scatter_plt(fname, asset_class, two_features, ax)
#svm_object.scoring_selection_gridCV(fname, asset_class, all_cols, ax)
#svm_object.hard_vs_soft_margin(fname, asset_class, two_features)
#svm_object.cross_validation_test(fname, asset_class, feature_combination, ax)
#print(svm_object.pnl_backtesting(fname, asset_class, feature_combination).head(20))
#plt.show()