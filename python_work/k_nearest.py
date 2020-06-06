import pandas as pd 
import numpy as np
from random import choices
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pandas.plotting import register_matplotlib_converters
from math import sqrt, pow
from yahoo_data_prep import create_features, get_colums_names, get_dates
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit, KFold, GridSearchCV, cross_validate
from sklearn.metrics import confusion_matrix
register_matplotlib_converters()

#Define function to perform scaling of features.
def scaling_function (dataframe):
    """User defined function to perform scaling on feature vectors from a dataset; given as a pandas dataframe.
    """
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
    """User defined function to compute the l nearest neighbors from first principles. Metric is the Euclidean one.
    """
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



#Function to compute powerset of a list.
def powerset(s):
    """Function to compute the power set of a given list, s. 
    """
    x = len(s)
    power_set = []
    for i in range(1 << x):
        subset = [s[j] for j in range(x) if (i & (1 << j))]
        power_set.append(subset)

    return power_set 


class KNNClassifier(KNeighborsClassifier):
    """Class to implement various methods to use on top of the KNeighborsClassifier methods.
    """
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
        #Scale the training data.
        scaled_df = scaler.fit_transform(X_train)

        return scaled_df, y_classifier

    def fit_test_model (self, fname, asset_class, cols):
        """Function used solely to invoke the fit() method of the subclass KNeighborsClassifier. 
        """
        X_train_scaled, y_classifier = self.scaling_function(fname, asset_class, cols)
        self.fit(X_train_scaled, y_classifier)

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
        
        self.fit_test_model(fname, asset_class, cols)
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

    def get_optimal_k (self, fname, asset_class, cols):
        """Use this function to determine the optimal k using the score function.
        """
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
        """Plot the decision boundary of the classifier. Cols has to be a list of two colms and no more.
        """
        self.fit_test_model(fname, asset_class, cols)
        cmap_light = ListedColormap(['orange', 'cornflowerblue'])
        x_min, x_max = 0, 0.25
        y_min, y_max = -0.6, 0.8
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.005), np.arange(y_min, y_max, 0.005))
        classified_from_model = self.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.pcolormesh(xx, yy, classified_from_model, cmap=cmap_light)

    def get_feature_scatter_plt (self, fname, asset_class, cols, ax):
        """Function to plot scatters with emphasize on highlighting points from different classes.
        """
        df = create_features(fname, asset_class)
        df = df[df['return_sign'] != 0.0]  # Remove any zero returns to avoiding multi-class classification.

        #Seperate points into up/down moves.
        up_moves = df[df['return_sign'] == 1.0]
        down_moves = df[df['return_sign'] == -1.0]
        ax.scatter(up_moves[cols[0]], up_moves[cols[1]], color='g', s=1, alpha=1, label='Up')
        ax.scatter(down_moves[cols[0]], down_moves[cols[1]], color='r', s=1, alpha=1, label='Down')
        ax.legend(fontsize=10)
        ax.set_title('Decision Boundary')
        ax.set_xlabel(cols[0])
        ax.set_ylabel(cols[1])


    def metric_comparison (self, fname, asset_class, cols, metrics):
        """Compare the accuracy of the classifier when varying the metric as contained in the metrics list, care must be taken when dealing with the mahalanobis metric.
        """
        data_list = []
        for metric in metrics:
            self.metric = metric
            xdata, y = self.scaling_function(fname, asset_class, cols)
            if self.metric is 'mahalanobis':
                covariance_matrix = np.cov(xdata)
                self.metric_params = {'V':covariance_matrix}
            else:
                pass

            self.fit_test_model(fname, asset_class, cols)
            data_list.append(self.score(xdata, y))

        data_df = pd.DataFrame({'Metric':metrics, 'Accuracy Score':data_list})

        return data_df

    def scoring_selection_gridCV (self, fname, asset_class, cols, ax, nested_CV):
        """Perform scoring and selection of best estimator from a range of parameters. Try different combinations of colmns.
        """
        #Nested cross_validation is employed here. 
        params_grid = {'n_neighbors': [2, 3, 5, 10, 20, 50, 100]}
        cv_1 = KFold(n_splits=3, shuffle=False, random_state=1)
        cv_2 = KFold(n_splits=3, shuffle=False, random_state=1)
        #cols_subsets = [cols, cols[:3], cols[3:], cols[-3:], cols[:-3]]
        cols_subsets = powerset(cols)
        #cols_subsets = [elem for elem in powerset(cols) if len(elem) not in [0, 1]]  # exclude empty and one elem subsets. These cause issues 
        #Create dictionary for storing scores.
        scores_array = {}
        index = 0
        best_params = []

        for cols in cols_subsets:
            
            #Handle case for when metric is 'mahalanobis' and empty sets given by cols.
            if self.metric is 'mahalanobis' and (len(cols) > 1):
                X, y = self.scaling_function(fname, asset_class, cols)
                covariance_matrix = np.cov(X)
                self.metric_params = {'V':covariance_matrix, 'VI':np.linalg.inv(covariance_matrix)}
            elif self.metric is 'mahalanobis' and len(cols) <= 1:
                index += 1
                scores_array[index] = 0
                best_params.append(0)
                continue
            elif len(cols) == 0:
                index += 1
                scores_array[index] = 0
                best_params.append(0)
                continue              
            else:
                X, y = self.scaling_function(fname, asset_class, cols)
                pass

            #Create object of GridSearchCV to use for scoring. 
            clf = GridSearchCV(estimator = self, param_grid=params_grid, cv = cv_1, refit=True)

            if nested_CV is True:
                score = cross_val_score(clf, X=X, y=y, cv=cv_2)
                index += 1
                scores_array[index] = score.mean()*100
            else:
                score = clf.fit(X=X, y=y).best_score_
                index += 1
                scores_array[index] = score*100
                best_params.append(clf.best_params_['n_neighbors'])

        x = list(scores_array.keys()); y = scores_array.values()

        ax.scatter(x, y, color='r', label='score')
        ax.scatter(x, best_params, color='g', label='Best n_neighbors')
        ax.legend()

    def pnl_backtesting (self, fname, asset_class, cols):
        """Perform PnL backtesting to check how accurate is the PnL predicted by the model is given previous realised price returns.
        """
        X, y = self.get_train_data(fname, asset_class, cols)

        #Split the data into test and training data and train the model on the training data.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
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

        df = pd.DataFrame({'Prob-Down':probability_down, 'Prob-Up':probability_up, 'Predic-Move':predicted_direction, 'Real-Move':y_test, 'Daily PnL':realised_daily_profit})
        #print(df.head(30))

        #Plot scatter plots for probabilities.
        #color_code = np.multiply(predicted_direction, y)   # 1 if probability UP was correct
        #cmap = ListedColormap(['r', 'g'])  # Red means incorrect prediction.
        #ax.scatter(xdata, probability_up, c=color_code, cmap=cmap)
        #ax.scatter(xdata, probability_down, c=color_code, cmap=cmap)

        return df

####################################################################################################################################################################################
#
#  Compute the actual k-nearest-neighbors from real data.
#
####################################################################################################################################################################################


#Setup model parameters.
#fname = "currency_data.xlsx"
fname = "index_data.xlsx"
asset_class = 'SP500'
all_cols = get_colums_names(fname, asset_class)
metric = ['manhattan', 'euclidean', 'mahalanobis']

#Determine which combination of features to investigate; select one from all the possible combinations in the powerset.
feature_combination = powerset(all_cols)[205]
#ax = plt.gca()

#Create KNNClassifier object, best parameters to use depends on the output of the GridSearchCV class methods.
knn_object = KNNClassifier(n_neighbors=100, weights='uniform', metric=metric[1], algorithm='brute')

#knn_object.plot_decision_boundary(fname, asset_class, feature_combination, ax)
#knn_object.get_feature_scatter_plt(fname, asset_class, feature_combination, ax)
#accuracy_df =  knn_object.get_optimal_k(fname, asset_class, feature_combination)
#accuracy_df = knn_object.metric_comparison(fname, asset_class, feature_combination, metric)
#print(accuracy_df)
#knn_object.scoring_selection_gridCV(fname, asset_class, cols, ax, False)
#knn_object.cross_validation_test(fname, asset_class, feature_combination, ax)
#print(knn_object.pnl_backtesting(fname, asset_class, feature_combination).head(20))
#plt.show()