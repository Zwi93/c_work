"""Script to compare the three Classifiers and see which one gives a return closest to the actual return
"""

from k_nearest import KNNClassifier, get_colums_names, powerset
from logistic_regression import LogisticRegressionClassifier, powerset, get_colums_names, NaiveGaussianClassifier
from support_vector_machine import SVMClassifier, powerset, get_colums_names
from yahoo_data_prep import create_features
import matplotlib.pyplot as plt
import matplotlib as mat
import numpy as np

#Setup model parameters.
fname = "currency_data.xlsx"
#fname = "SA_equities.xlsx"
#fname = "index_data.xlsx"
#fname = "bitcoin_data.xlsx"
asset_class = 'GBPUSD'
all_cols = get_colums_names(fname, asset_class)
metric = ['manhattan', 'euclidean', 'mahalanobis']

#Determine which combination of features to investigate; select one from all the possible combinations in the powerset.
feature_combination = powerset(all_cols)[205]

#Create KNNClassifier object, best parameters to use depends on the output of the GridSearchCV class methods.
#knn_object = KNNClassifier(n_neighbors=10, weights='uniform', metric=metric[1], algorithm='brute')
#df1 = knn_object.pnl_backtesting(fname, asset_class, feature_combination)

#Create LogisticRegressionClassifier object.  # high C corresponds to no regularization.
logit_object = LogisticRegressionClassifier(C=50, solver='liblinear', penalty='l2')  
df2 = logit_object.pnl_backtesting (fname, asset_class, feature_combination)

#Create SVM object. High C means hard margins, and hence takes longer to solve the optimization problem.
svm_object = SVMClassifier(C=1, kernel='linear', cache_size = 1000)
df3 = svm_object.pnl_backtesting(fname, asset_class, feature_combination)

#Dataframe carrying all info about features, especially the actual realised return, that will be compared with the predicted return.
df = create_features(fname, asset_class)
df = df[-df2.shape[0]:]

#Put all predicted PnL for each classifier in the one dataframe df, and then plot all to comapre.
#df['pred_ret_knn'] = df1['Daily PnL']
df['pred_ret_svm'] = df3['Daily PnL']
df['pred_ret_logit'] = df2['Daily PnL']
df[['pred_ret_svm', 'pred_ret_logit']].cumsum().apply(np.exp).plot(figsize=(15, 10))
plt.savefig('USDZAR.png')

