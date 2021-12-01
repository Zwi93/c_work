"""
Module stuff here, basically a script to do ML for FPL......

@athor   : Zwi Mudau 
Date     : 2021/02/08  


"""

import os
import numpy as np
import pandas as pd 
from sklearn import svm
import sklearn.linear_model as skl_lm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit, KFold, GridSearchCV, cross_validate
from sklearn.metrics import confusion_matrix
from sklearn.svm import l1_min_c
import matplotlib.pyplot as plt
import matplotlib as mat
from fpl import FPL
import aiohttp
import asyncio

#pd.set_options()

#Function to compute powerset of a list.
def powerset(s):
    x = len(s)
    power_set = []
    for i in range(1 << x):
        subset = [s[j] for j in range(x) if (i & (1 << j))]
        power_set.append(subset)

    return power_set 

def collect_players_stats (directory):
    "Function to read players data from the csv located on the paths provided."
    dataframe_lists = []

    for name in directory:
    
        for root, dirs, files in os.walk(name):
    
            pathname = root + "/gw.csv"
        
            try:
                df = pd.read_csv(pathname)
                dataframe_lists.append(df)

            except:
                continue
    
    players_stats = pd.concat(dataframe_lists, sort=False)  # This returns all columns, even the ones that don't match between the diff dfs.
    players_stats.to_csv('pl_players_stats_detailed.csv', index=None)

    return players_stats


def compute_seasons_rolling_stats (directories):
    "Function to read the csv data for each player and compute the rolling gameweeks' stats and save into a file."
    dataframe_collector = []
    
    #1st read in the data from the location.
    for name in directories:
    
        for root, dirs, files in os.walk(name):
    
            pathname = root + "/gw.csv"
        
            try:
                df = create_model_features(pathname, False)
                dataframe_collector.append(df)
                
            except:
                continue

    players_stats = pd.concat(dataframe_collector, join="inner")  # This ensures only common columns are returned.
    #players_stats.drop()  # Drop index column.
    players_stats.to_csv('/home/zwi/zwi_work/python_work/database/pl_players_rolling_stats.csv', index=None)


def create_model_features (pathname, in_season):
    "Function to compute the feature vectors for the ML model from the provided path name to a player's csv data."
    dataframe = pd.read_csv(pathname)
    rows = dataframe.shape[0]
    cols = dataframe.shape[1]

    index = 1

    #Lists have zero frist element at the start of the season. This can be extended further by using previous seasons data.
    points_list = [0]
    points_per90_list = [0]
    chances_created_list = [0]
    bonus_points_list = [0]
    solid_defense_list = [0]
    creativity_list = [0]
    defense_errors_list = [0]
    goals_conceded_list = [0]
    goals_scored_list = [0]
    saves_list = [0]
    crosses_list = [0]
    threat_list = [0]
    ict_list = [0]
    minutes_list = [0]
    assists_list = [0]
    goals_involvement_list = [0]
    points_return_list = [0]

    #Loop ends when index is 38, no need to exclude the last game of the season.
    while index <= rows:   
        slice_df = dataframe[:index]
        points_colmn = slice_df['total_points']
        points_per90 = slice_df[slice_df['minutes'] != 0]['total_points']
        #big_chances_created_per90 = slice_df[slice_df['minutes'] != 0]['big_chances_created']
        bonus_per90 = slice_df[slice_df['minutes'] != 0]['bonus']
        #clearances_blocks_interceptions_per90 = slice_df[slice_df['minutes'] != 0]['clearances_blocks_interceptions']
        creativity_per90 = slice_df[slice_df['minutes'] != 0]['creativity']
        #errors_leading_to_goal_attempt_per90 = slice_df[slice_df['minutes'] != 0]['errors_leading_to_goal_attempt']
        goals_conceded_per90 = slice_df[slice_df['minutes'] != 0]['goals_conceded']
        goals_scored_per90 = slice_df[slice_df['minutes'] != 0]['goals_scored']
        saves_per_90 = slice_df[slice_df['minutes'] != 0]['saves']
        #open_play_crosses_per90 = slice_df[slice_df['minutes'] != 0]['open_play_crosses']
        threat_per90 = slice_df[slice_df['minutes'] != 0]['threat']
        ict_per90 = slice_df[slice_df['minutes'] != 0]['ict_index']
        minutes_per90 = slice_df[slice_df['minutes'] != 0]['minutes']
        assist_per90 = slice_df[slice_df['minutes'] != 0]['assists']

        if slice_df['minutes'].mean() > 0.0:  # Cater for players who didn't play entire season.
        
            average_points = points_colmn.mean()
            average_points_per90 = points_per90.mean()
            #average_chances_per90 = big_chances_created_per90.mean()
            average_bonus_per90 = bonus_per90.mean()
            #average_clearances_blocks_interceptions_per90 = clearances_blocks_interceptions_per90.mean()
            average_creativity_per90 = creativity_per90.mean()
            #average_errors_per90 = errors_leading_to_goal_attempt_per90.mean()
            average_goals_conceded_per90 = goals_conceded_per90.mean()
            average_goals_scored_per90 = goals_scored_per90.mean()
            average_saves_per_90 = saves_per_90.mean()
            #average_open_play_crosses_per90 = open_play_crosses_per90.mean()
            average_threat_per90 = threat_per90.mean()
            average_ict_per90 = ict_per90.mean()
            average_minutes_per90 = minutes_per90.mean()
            average_assist_per90 = assist_per90.mean()
            goal_involvement_per90 = assist_per90.sum() + goals_scored_per90.sum()
            average_goal_involvement_per90 = goal_involvement_per90/slice_df['minutes'].shape[0]
            
            if index > 1:
                size_array = points_per90.size
                temp_list = points_per90.tolist()
                overall_season_pts = np.array(temp_list)[:size_array].sum()
                #overall_season_pts = points_per90[:size_array - 1].sum()
                #print(points_per90.tolist())
                #print(overall_season_pts)
                #points_return = points_per90.tolist()[size_array - 1]/overall_season_pts
            else:
                points_return = points_per90[0] 
        
        else:

            average_points = 0
            average_points_per90 = 0
            #average_chances_per90 = 0
            average_bonus_per90 = 0
            #average_clearances_blocks_interceptions_per90 = 0
            average_creativity_per90 = 0
            #average_errors_per90 = 0
            average_goals_conceded_per90 = 0
            average_goals_scored_per90 = 0
            average_saves_per_90 = 0
            #average_open_play_crosses_per90 = 0
            average_threat_per90 = 0
            average_ict_per90 = 0
            average_minutes_per90 = 0
            average_assist_per90 = 0
            #goal_involvement_per90 = assit_per90.sum() + goals_scored_per90.sum()
            average_goal_involvement_per90 = 0
            points_return  = 0
        
        points_list.append(average_points)
        points_per90_list.append(average_points_per90)
        #chances_created_list.append(average_chances_per90)
        bonus_points_list.append(average_bonus_per90)
        #solid_defense_list.append(average_clearances_blocks_interceptions_per90)
        creativity_list.append(average_creativity_per90)
        #defense_errors_list.append(average_errors_per90)
        goals_conceded_list.append(average_goals_conceded_per90)
        goals_scored_list.append(average_goals_scored_per90)
        saves_list.append(average_saves_per_90)
        #crosses_list.append(average_open_play_crosses_per90)
        threat_list.append(average_threat_per90)
        ict_list.append(average_ict_per90)
        minutes_list.append(average_minutes_per90)
        assists_list.append(average_assist_per90)
        goals_involvement_list.append(average_goal_involvement_per90)
        #points_return_list.append(points_return)
        
        index += 1

    dataframe.loc[rows] = np.zeros(cols)
    
    dataframe['average_points'] = points_list
    dataframe['average_points_per90'] = points_per90_list
    #dataframe['average_chances_per90'] = chances_created_list
    dataframe['average_bonus_per90'] = bonus_points_list
    #dataframe['average_clearances_blocks_interceptions_per90'] = solid_defense_list
    dataframe['average_creativity_per90'] = creativity_list
    #dataframe['average_errors_per90'] = defense_errors_list
    dataframe['average_goals_conceded_per90'] = goals_conceded_list
    dataframe['average_goals_scored_per90'] = goals_scored_list
    dataframe['average_saves_per_90'] = saves_list
    #dataframe['average_open_play_crosses_per90'] = crosses_list
    dataframe['average_threat_per90'] = threat_list
    dataframe['average_ict_per90'] = ict_list
    dataframe['average_minutes_per90'] = minutes_list
    dataframe['average_assist_per90'] = assists_list
    dataframe['average_goal_involvement_per90'] = goals_involvement_list
    #dataframe['points_return'] = points_return_list
    ylabel_df = dataframe['goals_scored'] + dataframe['assists']

    dataframe['ylabel_1'] = ylabel_df#.shift(-1)

    dataframe.dropna(inplace=True)

    #print(dataframe)
    if in_season is True:
        return dataframe.tail(1)
    elif in_season is False:
        return dataframe[:rows]
    else:
        print('check in_season parameter')

def digitize_array (array, number):
    "Function to convert array to zeros and ones; any number greater or equals to number parameter is cut down to one. Zero remains zero."

    new_array = np.ones(array.shape[0])

    index = 0

    for entry in array:
        if (number - entry) <= 0:
            new_array[index] = 1
        else:
            new_array[index] = 0
        index += 1

    return new_array

def visualize_football_data (filename, col_name):
    "Function to perform rudimentary checks on the quality of the data for football stats"
    array = pd.read_csv(filename, names=col_name)
    
    plt.scatter(array)
    plt.show()

async def get_season_stats ():
    "Function to obtain player's game by game stats and save to relevant files"
    session = aiohttp.ClientSession()
    fpl = FPL(session)

    players_data = await fpl.get_players(include_summary=True, return_json=True)
    
    #First update the player's history using data from FPL site.
    for player in players_data:

        player_name = player['first_name']
        player_surname = player['second_name']
        player_id = str(player['history'][0]['element'])

        fname = "/home/zwi/zwi_work/Fantasy-Premier-League/data/2021-22/players/" + player_name + "_" + player_surname + "_" + player_id +  "/gw.csv"
        #stream_to_file = open(fname, "w+")
        player_df = pd.DataFrame(player['history'])
        try:
            player_df.to_csv(fname, index=None, mode="w+")
        
        except FileNotFoundError:
            #print(player_df.to_csv())
            continue

    #Next pull up the updated data and compute season's stats
    dataframe_collector = []
    for player in players_data:

        player_name = player['first_name']
        player_surname = player['second_name']
        player_id = str(player['history'][0]['element'])

        fname = "/home/zwi/zwi_work/Fantasy-Premier-League/data/2021-22/players/" + player_name + "_" + player_surname + "_" + player_id +  "/gw.csv"
        
        try:
            player_rolling_stats = create_model_features(fname, True)  # This will give the player's rolling stats going into the next match.
        
        except FileNotFoundError:
            continue

        player_rolling_stats['player_id'] = player_id
        player_rolling_stats['player_name'] = player_name
        player_rolling_stats['player_surname'] = player_surname
        dataframe_collector.append(player_rolling_stats)
        #print(np.array(player_rolling_stats))
    consolidated_df = pd.concat(dataframe_collector)#, columns=player_rolling_stats.columns)
    #consolidated_df.drop()

    await session.close()
    
    return consolidated_df


rootdir = ["/home/zwi/zwi_work/Fantasy-Premier-League/data/2016-17", "/home/zwi/zwi_work/Fantasy-Premier-League/data/2017-18", "/home/zwi/zwi_work/Fantasy-Premier-League/data/2018-19",
"/home/zwi/zwi_work/Fantasy-Premier-League/data/2019-20", "/home/zwi/zwi_work/Fantasy-Premier-League/data/2020-21"]

#fname = "/home/zwi/zwi_work/Fantasy-Premier-League/data/2018-19/players/Adam_Lallana_250/gw.csv"
#fname = "/home/zwi/zwi_work/Fantasy-Premier-League/data/2020-21/players/Pierre-Emerick_Aubameyang_4/gw.csv"
#print(create_model_features(fname, False))
#visualize_football_data(fname, '')
#players_stats = pd.read_csv('pl_players_stats_detailed.csv')
#asyncio.get_event_loop().run_until_complete(get_season_stats())
#print(players_stats.columns)
#compute_seasons_rolling_stats(rootdir)


#########################################################################################################################################################################
#
#  Machine Learning Class definitions begin here
#
#########################################################################################################################################################################

class FPLSVMClassifier (svm.SVC):
    "Class to define the object for the FPL classifier with base class Support Vector Classifier. Various functions are defined here catering for different jobs."
    def obtain_training_data (self, cols, fname):
        "Function to load the training data for the ML model"

        #nrows is 100148 from the original csv.
        df = pd.read_csv(fname)#, nrows=10000)
        X_train = df.loc[:, cols]
        y_classifier = digitize_array(df.ylabel_1, 1)

        #print(len(y_classifier))
        return X_train, y_classifier

    def fit_test_model (self, cols, fname):
        "Function to test the model on the data to be loaded."
        #Collecting the training data.
        training_xdata, training_ydata = self.obtain_training_data (cols, fname)

        self.probability = True
        self.fit(training_xdata, training_ydata)

        test_array = np.array([0, 0, 0, 0]).reshape(1, -1)
        print(self.predict_proba(test_array))

    def scoring_selection_gridCV (self, cols, fname):
        """Perform scoring and selection of best estimator from a range of parameters. Try different combinations of colmns.
        """
        params_grid = {'C': [0.001, 0.002, 0.005, 0.008, 0.009]}
        cv_1 = KFold(n_splits=3, shuffle=False)#, random_state=1)
        cv_2 = KFold(n_splits=3, shuffle=False)#, random_state=1)
        cols_subsets = powerset(cols)[1:]

        #Create dictionary for storing scores.
        scores_array = {}
        index = 0

        for cols in cols_subsets:
            #Create object of GridSearchCV to use for scoring. 
            clf = GridSearchCV(estimator = self, param_grid=params_grid, cv = cv_1)
            training_xdata, training_ydata = self.obtain_training_data(cols, fname)
            nested_score = cross_val_score(clf, X=training_xdata, y=training_ydata, cv=cv_2)
            index += 1
            scores_array[index] = nested_score.mean()

        x = list(scores_array.keys()); y = scores_array.values()

        plt.scatter(x, y)
        plt.show()
    
    
class FPLogisticRegressionClassifier (skl_lm.LogisticRegression):
    ""
    def obtain_training_data (self, cols, fname):
        "Function to load the training data for the ML model"
        df = pd.read_csv(fname)#, nrows=1000)
        X_train = df.loc[:, cols]
        y_classifier = digitize_array(df.ylabel_1, 1)

        #print(len(y_classifier))
        return X_train, y_classifier

    def get_minimum_c (self, cols, fname):
        """Function to obtain the minimum c parameter. any value smaller than this yields a model with 0 coefficients.
        """
        training_xdata, training_ydata = self.obtain_training_data (cols, fname)

        #To determine the minimum C that gives a non 'null' model, only applicable when applying l1 penalty.
        min_c = l1_min_c(training_xdata, training_ydata, loss='log')

        return min_c

    def fit_test_model (self, cols, fname):
        """Function to fit model without cross validation.
        """
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
        training_xdata, training_ydata = self.obtain_training_data (cols, fname)

        self.probability = True
        self.fit(training_xdata, training_ydata)

    def predict_nxtgw_top_players (self, cols, fname, players_df):
        "Function to take in model's input with unknown labels and predict the class of these inputs"
        self.fit_test_model(cols, fname)

        #test_array = np.array([0, 0, 0, 0]).reshape(1, -1)
        players_goal_assist_probability = self.predict_proba(players_df[cols])

        probability_goal_assist_list = []
        for probability in players_goal_assist_probability:
            probability_goal_assist_list.append(probability[1])

        players_df['goal_assist_proba'] = probability_goal_assist_list
        
        #Next pick only the players with a probability higher than 0.10
        #condition = 
        players_df.sort_values(by=['goal_assist_proba'], ascending=True)
        players_df.to_csv("top_perfromers_predictions.csv")

        #return players_df 

    def scoring_selection_gridCV (self, cols, fname):
        """Perform scoring and selection of best estimator from a range of parameters. Try different combinations of colmns.
        """
        params_grid = {'C': [100, 200, 300, 400, 500]}
        cv_1 = KFold(n_splits=3, shuffle=False) #, random_state=1)
        cv_2 = KFold(n_splits=3, shuffle=False) #, random_state=1)  # No effect if shuffle is false. 
        cols_subsets = powerset(cols)[1:]

        #Create dictionary for storing scores.
        scores_array = {}
        index = 0

        for cols in cols_subsets:
            #Create object of GridSearchCV to use for scoring. 
            clf = GridSearchCV(estimator = self, param_grid=params_grid, cv = cv_1)
            training_xdata, training_ydata = self.obtain_training_data(cols, fname)
            nested_score = cross_val_score(clf, X=training_xdata, y=training_ydata, cv=cv_2)
            index += 1
            scores_array[index] = nested_score.mean()

        x = list(scores_array.keys()); y = scores_array.values()

        plt.scatter(x, y)
        plt.show()


cols = ['average_points', 'average_points_per90', 'average_bonus_per90', 'average_creativity_per90', 'average_goals_conceded_per90', 'average_goals_scored_per90', 
        'average_saves_per_90', 'average_threat_per90', 'average_ict_per90', 'average_minutes_per90', 'average_assist_per90', 'average_goal_involvement_per90']

fname = '/home/zwi/zwi_work/python_work/database/pl_players_rolling_stats.csv'
test_vector = asyncio.get_event_loop().run_until_complete(get_season_stats())
svm_object = FPLSVMClassifier(C=0.005, kernel='linear', cache_size = 1000)
#svm_object.fit_test_model(cols, fname)
#svm_object.obtain_training_data(cols, fname)
#svm_object.scoring_selection_gridCV(cols, fname)
logit_object = FPLogisticRegressionClassifier(C=100, solver='liblinear', penalty='l2')
#logit_object.fit_test_model(cols, fname)
#logit_object.scoring_selection_gridCV(cols, fname)
logit_object.predict_nxtgw_top_players(cols, fname, test_vector)