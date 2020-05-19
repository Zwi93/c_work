import pandas as pd 
import numpy as np
from random import choices
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from math import sqrt, pow
from yahoo_data_prep import create_features, get_colums_names
from matplotlib.colors import ListedColormap

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


#Function to compute powerset of a list.
def powerset(s):
    x = len(s)
    power_set = []
    for i in range(1 << x):
        subset = [s[j] for j in range(x) if (i & (1 << j))]
        power_set.append(subset)

    return power_set 


class KNNClassifier(KNeighborsClassifier):
    def get_train_data (self, fname, asset_class, cols):
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.
        X_train = df.loc[:, cols]
        y_classifier = df.return_sign

        return X_train, y_classifier

    def scaling_function (self, fname, asset_class, cols):
        scaler = StandardScaler()
        X_train, y_classifier = self.get_train_data(fname, asset_class, cols)
        #Scale the training data.
        scaled_df = scaler.fit_transform(X_train)

        return scaled_df, y_classifier

    def fit_test_model (self, fname, asset_class, cols):
        X_train_scaled, y_classifier = self.scaling_function(fname, asset_class, cols)
        self.fit(X_train_scaled, y_classifier)

    def get_optimal_k (self, fname, asset_class, cols):
        #Use this function to determine the optimal k using the score function.
        k_params = [2, 3, 4, 5, 10, 20, 50, 100, 200, 500, 600, 1000]
        accuracy_score = []
        for k in k_params:
            self.n_neighbors = k
            xdata, y = self.scaling_function(fname, asset_class, cols)
            self.fit_test_model(fname, asset_class, cols)
            accuracy_score.append(self.score(xdata, y))

        data_dict = {'K Parameter':k_params, 'Accuracy Score':accuracy_score}
        data_df = pd.DataFrame(data_dict)

        return data_df

    def plot_decision_boundary (self, fname, asset_class, cols, ax):
        #Plot the decision boundary of the classifier. Cols has to be a list of two colms and no more.
        self.fit_test_model(fname, asset_class, cols)
        cmap_light = ListedColormap(['orange', 'cornflowerblue'])
        x_min, x_max = -0.2, 0.2
        y_min, y_max = -0.2, 0.2
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.005), np.arange(y_min, y_max, 0.005))
        classified_from_model = self.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.pcolormesh(xx, yy, classified_from_model, cmap=cmap_light)

    def get_feature_scatter_plt (self, fname, asset_class, cols, ax):
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.

        #Seperate points into up/down moves.
        up_moves = df[df['return_sign'] == 1.0]
        down_moves = df[df['return_sign'] == -1.0]
        ax.scatter(up_moves[cols[0]], up_moves[cols[1]], color='r', s=10)
        ax.scatter(down_moves[cols[0]], down_moves[cols[1]], color='b', s=10)

    def metric_comparison (self, fname, asset_class, cols, metrics):
        #Compare the accuracy of the classifier when varying the metric as contained in the metrics list.
        data_dict = {}
        for metric in metrics:
            self.metric = metric
            xdata, y = self.scaling_function(fname, asset_class, cols)
            if self.metric is 'mahalanobis':
                covariance_matrix = np.cov(xdata)
                self.metric_params = {'V':covariance_matrix}
            else:
                pass

            self.fit_test_model(fname, asset_class, cols)
            data_dict[metric] = self.score(xdata, y)

        #data_df = pd.DataFrame(data_dict)

        return data_dict

    def scoring_selection_gridCV (self, fname, asset_class, cols, ax):
        #Perform scoring and selection of best estimator from a range of parameters. Try different combinations of clomns.
        params_grid = {'n_neighbors': [2, 3, 5, 10, 20, 50, 100]}
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
cols = ['ret_1', 'ret_2']
#asset_class = 'USDZAR'
asset_class = 'SP500'
all_cols = get_colums_names(fname, asset_class)
ax = plt.gca()

#Create KNNClassifier object.
metric = ['manhattan', 'euclidean', 'mahalanobis']
knn_object = KNNClassifier(n_neighbors=3, weights='uniform', metric=metric[1], algorithm='brute')
#knn_object.plot_decision_boundary(fname, asset_class, cols, ax)
#knn_object.get_feature_scatter_plt(fname, asset_class, cols, ax)
#accuracy_df =  knn_object.get_optimal_k(fname, asset_class, all_cols)
#accuracy_df = knn_object.metric_comparison(fname, asset_class, all_cols, metric)
#print(accuracy_df)
#plt.show()