import pandas as pd 
import numpy as np
from random import choice
import sklearn.linear_model as skl_lm
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import yfinance as yf
from pandas_datareader import data, wb 
from yahoo_data_prep import create_features

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

fname = "index_data.xlsx"
df = create_features(fname, "VIX")

df = df[df['return_sign'] != 0.0]

#X_train = df.SMA.values.reshape(-1, 1)
X_train = df[['ret_1', 'ret_2']]
y_classifier = df.return_sign
#X_test = np.arange(df.Balance.min(), df.Balance.max()).reshape(-1, 1)
#X_test = np.arange(1, 700).reshape(-1, 1)
#X_test = np.arange(df.ret_1.min(), df.ret_1.max()).reshape(-1, 1)
X_test = df[['ret_1', 'ret_2']]

clf = skl_lm.LogisticRegression(solver='newton-cg')
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