import pandas as pd 
import numpy as np
from random import choice
import sklearn.linear_model as skl_lm
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit, KFold, GridSearchCV, cross_validate 
from yahoo_data_prep import create_features, get_colums_names, get_dates 
from sklearn.svm import l1_min_c
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


class LogisticRegressionClassifier (skl_lm.LogisticRegression):
    def get_train_data (self, fname, asset_class, cols):
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
        X_train = df.loc[:, cols]
        y_classifier = df.return_sign

        return X_train, y_classifier

    def get_minimum_c (self, fname, asset_class, cols):
        
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        #To determine the minimum C that gives a non 'null' model, only applicable when applying l1 penalty.
        min_c = l1_min_c(X_train, y_classifier, loss='log')

        return min_c

    def fit_test_model (self, fname, asset_class, cols):
        #Function to fit model without cross validation. 
        #determine which penalty is being applied.
        penalty = self.penalty

        #L1 loss function gives null model if C is too small. We can modify it here.
        if penalty is 'l1':
            min_c = self.get_minimum_c(fname, asset_class, cols)
            if self.C < 100*min_c:
                self.C = 100*min_c
            else:
                pass
        else:
            pass
        #Perform cross_validation on the model.
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)

        self.fit(X_train, y_classifier)

    def fit_test_CV (self, fname, asset_class, cols):
        #perform cross_validation to yield best output for any metric.
        X, y = self.get_train_data(fname, asset_class, cols)
        validated_model = cross_validate(self, X, y, cv=5, return_estimator=True)  # This is a dictionary object.
    
        return validated_model

    def classify_data (self, fname, asset_class, cols, test_data, ax):
        #Predict class for given array of samples and plot the results on a scatter plot.
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        
        self.fit_test_model(fname, asset_class, cols)
        unvalidated_classified_data = self.predict_proba(test_data)[:, 0]
        #matrix = confusion_matrix(y_classifier, unvalidated_classified_data)
        #print(matrix)
        
        ax.scatter(test_data[cols[0]], unvalidated_classified_data , color='b', s=20)

        validated_model = self.fit_test_CV(fname, asset_class, cols)
        best_models = validated_model['estimator']
        best_scores = validated_model['test_score']
        max_score = max(best_scores)

        for score, model in zip(best_scores, best_models):
            if score == max_score:
                classified_test_data = model.predict_proba(test_data)[:, 0]
                #matrix = confusion_matrix(y_classifier, classified_test_data)
                #print(matrix)
            else:
                pass

        x_data1 = test_data[cols[0]]
        x_data2 = X_train[cols[0]]

        #To be able to plot test data must be 2d, higher dimensions impossible to plot.
        ax.scatter(x_data1, classified_test_data, color='r', s=10)
        ax.scatter(x_data2, y_classifier, color='orange')

    def get_coefficients (self, fname, asset_class, cols):
        #Examine the coefficients.
        self.fit_test_model(fname, asset_class, cols)
        coefficients = self.coef_
        return coefficients

    def compare_l1_l2(self, fname, asset_class, cols):
        #Compare the coefficients of different loss functions as we vary the C parameter.
        C_parameters = np.arange(1, 3)
        collect_c_params = []
        l1_coeff = []
        l2_coeff = []
        for c in C_parameters:
            self.C = c
            colm_no = len(cols)
            self.penalty = 'l1'
            coeff1 = self.get_coefficients(fname, asset_class, cols)[0]
            self.penalty = 'l2'
            coeff2 = self.get_coefficients(fname, asset_class, cols)[0]
            for i in range(colm_no):     
                l1_coeff.append(coeff1[i])
                l2_coeff.append(coeff2[i])
                collect_c_params.append(c)

        data_dict = {'C Parameter':collect_c_params, 'L1 Coefficients':l1_coeff, 'L2 Coefficients':l2_coeff}

        data_table = pd.DataFrame(data=data_dict)

        return data_table

    def scoring_selection_gridCV (self, fname, asset_class, cols, ax):
        #Perform scoring and selection of best estimator from a range of parameters. Try different combinations of clomns.
        params_grid = {'C': [100, 200, 300, 400, 500]}
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

    def pnl_backtesting (self, fname, asset_class, cols):
        #Perform PnL backtesting to check how accurate the path predicted by the model would have been given previous price returns.
        X, y = self.get_train_data(fname, asset_class, cols)
        self.fit(X, y)
        probability_down = self.predict_proba(X)[:, 0]
        probability_up = self.predict_proba(X)[:, 1]
        predicted_direction = self.predict(X)
        xdata = get_dates(fname, asset_class)
        df0 = create_features(fname, asset_class)
        df0 = df0[df0['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
        true_realised_return = df0['return']
        kelly_optimal_fraction = probability_up - probability_down
        realised_daily_profit = np.multiply(np.multiply(true_realised_return, predicted_direction), kelly_optimal_fraction)

        df = pd.DataFrame({'Prob-Down':probability_down, 'Prob-Up':probability_up, 'Predic-Move':predicted_direction, 'Real-Move':y, 'Daily PnL':realised_daily_profit})
        print(df.head(30))

        #Plot scatter plots for probabilities.
        #ax.scatter(xdata, probability_up, color='g')
        #ax.scatter(xdata, probability_down, color='r')

class NaiveGaussianClassifier(GaussianNB):
    def get_train_data (self, fname, asset_class, cols):
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
        X_train = df.loc[:, cols]
        y_classifier = df.return_sign

        return X_train, y_classifier
    
    def fit_test_model (self, fname, asset_class, cols):
        #Get full sample data points and then split it into training and test data.
        X, y = self.get_train_data(fname, asset_class, cols)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
        self.fit(X_train, y_train)
        accuracy_score = self.score(X_test, y_test)

        return accuracy_score

    def pnl_backtesting (self, fname, asset_class, cols):
        #Perform PnL backtesting to check how accurate the path predicted by the model would have been given previous price returns.
        X, y = self.get_train_data(fname, asset_class, cols)
        self.fit(X, y)
        probability_down = self.predict_proba(X)[:, 0]
        probability_up = self.predict_proba(X)[:, 1]
        predicted_direction = self.predict(X)
        xdata = get_dates(fname, asset_class)
        df0 = create_features(fname, asset_class)
        df0 = df0[df0['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
        true_realised_return = df0['return']
        kelly_optimal_fraction = probability_up - probability_down
        realised_daily_profit = np.multiply(np.multiply(true_realised_return, predicted_direction), kelly_optimal_fraction)

        #df = pd.DataFrame({'Prob-Down':probability_down, 'Prob-Up':probability_up, 'Predic-Move':predicted_direction, 'Real-Move':y, 'Daily PnL':realised_daily_profit})
        #print(df.head(30))

        #Plot scatter plots for probabilities.
        color_code = np.multiply(predicted_direction, y)   # 1 if probability UP was correct
        ax.scatter(xdata, probability_up, c=color_code)
        #ax.scatter(xdata, probability_down, color='r')

#fname = "currency_data.xlsx"
fname = "index_data.xlsx"
cols = ['ret_1', 'ret_2', 'ret_3']

#asset_class = 'USDZAR'
asset_class = 'SP500'
test_data = create_features(fname, asset_class)
test_data = test_data[test_data['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
all_cols = get_colums_names(fname, asset_class)
test_data = test_data.loc[:, all_cols]
ax = plt.gca()

#Create LogisticRegressionClassifier object.
logit_object = LogisticRegressionClassifier(C=1, solver='liblinear', penalty='l2')  # high C corresponds to no regularization.
#test_data = logit_object.get_train_data(fname, asset_class, cols)[0]
#logit_object.classify_data(fname, asset_class, all_cols, test_data, ax)
#coeff = logit_object.get_coefficients(fname, asset_class, cols)
#coef_table = logit_object.compare_l1_l2(fname, asset_class, cols)
gaussian_object = NaiveGaussianClassifier()
#accuracy_score = logit_object.fit_test_CV(fname, asset_class, all_cols)
#accuracy_score = gaussian_object.fit_test_model(fname, asset_class, cols, test_data)
#print(accuracy_score)
#logit_object.scoring_selection_gridCV(fname, asset_class, all_cols, ax) 
gaussian_object.pnl_backtesting (fname, asset_class, all_cols)
#plt.show()