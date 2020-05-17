import pandas as pd 
import numpy as np
from random import choices
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from math import sqrt, pow
from yahoo_data_prep import create_features

#Define function to perform scaling of features.
def scaling_function (dataframe):
    height_array = np.array(dataframe['Height'])
    weight_array = np.array(dataframe['Weight'])
    gender_array = np.array(dataframe['Gender'])
    mean_height = np.mean(height_array)
    mean_weight = np.mean(weight_array)
    std_height = np.std(height_array)
    std_weight = np.std(weight_array)

    ones_array = np.ones(weight_array.size)
    mean_height_array = ones_array*mean_height
    mean_weight_array = ones_array*mean_weight

    height_array = (height_array - mean_height_array)/std_height
    weight_array = (weight_array - mean_weight_array)/std_weight

    for i in range(weight_array.size):
        elem = gender_array[i]

        if elem == 'Male':
            gender_array[i] = 1
        else:
            gender_array[i] = 0

    new_array = np.array([gender_array, height_array, weight_array])

    return new_array

def k_nearest_neighbor(in_data, population, k):

    #in_data is a 2 tuple with 1st entry representing height and 2nd represennting weight. 
    popu_size = population.shape[1] 
    euclid_measure = np.ones(popu_size)

    for i in range(popu_size):
        euclid_measure[i] = sqrt(pow(in_data[0] - population[1, i], 2) + pow(in_data[1] - population[2, i], 2))

    categorized_data = np.array([euclid_measure, population[0, :]])
    categorized_data1 = np.sort(categorized_data)  # Sort from smallest to highest on distance column.
    highest_distance = categorized_data1[:, :k][0, :][-1]

    #Find, from ordered array, those with the distance less than the kth smallest distance.
    condition_for_k_nearest = np.where(categorized_data[0, :] <= highest_distance)
    category_of_k_nearest = categorized_data[1, :][condition_for_k_nearest]

    #Find percentage of each category from the k-nearest-neighbors.
    male_percentage = np.where(category_of_k_nearest == 1)
    male_percentage = male_percentage[0][0].size/category_of_k_nearest.size
    female_percentage = 1 - male_percentage

    return male_percentage, female_percentage


####################################################################################################################################################################################
#
#  Compute the actual k-nearest-neighbors from real data.
#
####################################################################################################################################################################################

'''
weight_height_data_0 = pd.read_csv('weight-height.csv')

weight_height_data_1 = scaling_function(weight_height_data_0)

weight_height_data = pd.DataFrame({'Gender': weight_height_data_1[0, :], 'Height': weight_height_data_1[1, :], 'Weight': weight_height_data_1[2, :]})

#SPlit data into male and female categories.
male_condition = weight_height_data['Gender'] == 1
male_data = weight_height_data[male_condition]
female_condition = weight_height_data['Gender'] == 0
female_data = weight_height_data[female_condition]

#Find the nearest points to in_data.
in_data = [-1.5, -1.02]
#k_neighbors = k_nearest_neighbor(in_data, weight_height_data_1, 10)
#print(k_neighbors)
'''

#Classify using in-built classes from sklearn.
#fname = "currency_data.xlsx"
fname = "index_data.xlsx"
#df = create_features(fname, "USDZAR")
df = create_features(fname, "SP500")
df = df[df['return_sign'] != 0.0]
cols = ['ret_1', 'ret_2']
X_train = df.loc[:, cols]
y_classifier = df.return_sign

scaler = StandardScaler()
scaled_df = scaler.fit_transform(X_train)   # Output is a numpy ndarray.
k_neighbors = 10
metric = ['manhattan', 'euclidean', 'mahalanobis']
clf = KNeighborsClassifier(k_neighbors, weights='uniform', metric=metric[1])
clf.fit(scaled_df, y_classifier)
X_test = df[['ret_1', 'ret_2']]
prob_of_upmove = clf.predict_proba(X_test)

fig = plt.figure(figsize=(10, 6))
x_data = df.ret_1.values.reshape(-1, 1)
plt.scatter(x_data, y_classifier, color = 'r')
plt.scatter(x_data, prob_of_upmove[:, 1], color='b')

plt.show()

'''
#Plot the results
fig = plt.figure(figsize=(10, 6))
plt.scatter(male_data['Height'], male_data['Weight'], color = 'b')
plt.scatter(female_data['Height'], female_data['Weight'], color = 'g')
plt.show()
'''
