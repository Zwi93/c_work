import pandas as pd 
import numpy as np
from random import choice
import sklearn.linear_model as skl_lm
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import yfinance as yf
from pandas_datareader import data, wb 
from yahoo_data_prep import create_features
from sklearn.svm import l1_min_c

'''
#Create fictional credit data.
income = np.sort(np.random.uniform(100, 1000, 1000))
balance = np.sort(np.random.uniform(1, 450, 1000))
ones_array = np.ones(750)
zeros_array = np.zeros(250)
ones_and_zeros = np.concatenate((ones_array, zeros_array))
default = np.ones(1000) 

for i in range(len(balance)):
    if i < 450:
        default[i] = choice([0, 0, 0, 0, 1])
    elif (i >= 450 and i <= 550):
        default[i] = choice([0, 1])
    else:
        default[i] = choice([0, 1, 1, 1, 1])

student = choice([0, 1])

#data = {'Default': default, 'Student': student, 'Balance': balance, 'Income': income}
#df = pd.DataFrame(data)

#fname = "index_data.xlsx"
fname = "currency_data.xlsx"
df = create_features(fname, "USDZAR")

df = df[df['return_sign'] != 0.0]

#X_train = df.SMA.values.reshape(-1, 1)
cols = ['ret_1', 'ret_2']
X_train = df[cols]
y_classifier = df.return_sign
#X_test = np.arange(df.Balance.min(), df.Balance.max()).reshape(-1, 1)
#X_test = np.arange(1, 700).reshape(-1, 1)
#X_test = np.arange(df.ret_1.min(), df.ret_1.max()).reshape(-1, 1)
X_test = df[['ret_1', 'ret_2']]

min_c = l1_min_c(X_train, y_classifier, loss='log')  # To determine the minimum C that gives a non 'null' model. 
clf = skl_lm.LogisticRegression(solver='liblinear', penalty='l1', C=1000*min_c)  
clf.fit(X_train, y_classifier)

print(clf.classes_)
print(clf.coef_)
print(clf.intercept_)

prob_of_upmove = clf.predict_proba(X_test)

fig = plt.figure(figsize=(10, 6))
x_data = df.ret_1.values.reshape(-1, 1)
plt.scatter(x_data, y_classifier, color = 'r')
plt.scatter(x_data, prob_of_upmove[:, 1], color='b')


clf_bayes = GaussianNB()
clf_bayes.fit(X_train, y_classifier)

prob_of_upmove_nb = clf_bayes.predict_proba(X_test)

plt.scatter(x_data, prob_of_upmove_nb[:, 1], color='orange')
plt.show()
'''

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

        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        self.fit(X_train, y_classifier)


    def classify_data (self, fname, asset_class, cols, test_data, ax):
        #Predict class for given array of samples and plot the results
        self.fit_test_model(fname, asset_class, cols)
        classified_test_data = self.predict(test_data)
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)

        x_data1 = test_data[cols[0]]
        x_data2 = X_train[cols[0]]

        ax.scatter(x_data1, classified_test_data, color='r')
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


#fname = "currency_data.xlsx"
fname = "index_data.xlsx"
cols = ['ret_1', 'ret_2']
#asset_class = 'USDZAR'
asset_class = 'SP500'
ax = plt.gca()

#Create LogisticRegressionClassifier object.
logit_object = LogisticRegressionClassifier(C=1, solver='liblinear', penalty='l2')
#test_data = logit_object.get_train_data(fname, asset_class, cols)[0]
#logit_object.classify_data(fname, asset_class, cols, test_data, ax)
#coeff = logit_object.get_coefficients(fname, asset_class, cols)
coef_table = logit_object.compare_l1_l2(fname, asset_class, cols)
print(coef_table) 
#plt.show()