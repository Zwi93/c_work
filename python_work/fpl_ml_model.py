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
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit, KFold, GridSearchCV, cross_validate

rootdir = ["/home/zwi/zwi_work/Fantasy-Premier-League/data/2016-17", "/home/zwi/zwi_work/Fantasy-Premier-League/data/2017-18", "/home/zwi/zwi_work/Fantasy-Premier-League/data/2018-19",
"/home/zwi/zwi_work/Fantasy-Premier-League/data/2019-20", "/home/zwi/zwi_work/Fantasy-Premier-League/data/2020-21"]

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
    
    players_stats = pd.concat(dataframe_lists, sort=False)
    players_stats.to_csv('pl_players_stats_detailed.csv')

    return players_stats


def compute_seasons_rolling_stats (directories):
    ""
    dataframe_collector = []
    
    #1st read in the data from the location.
    for name in directories:
    
        for root, dirs, files in os.walk(name):
    
            pathname = root + "/gw.csv"
        
            try:
                df = create_model_features(pathname)
                dataframe_collector.append(df)
                
            except:
                continue

    players_stats = pd.concat(dataframe_collector, sort=False)
    players_stats.to_csv('/home/zwi/zwi_work/python_work/database/pl_players_rolling_stats.csv')


def create_model_features (pathname):
    "Function to compute the feature vectors for the ML model."
    dataframe = pd.read_csv(pathname)
    rows = dataframe.shape[0]

    index = 1
    points_list = []
    points_per90_list = []
    chances_created_list = []
    bonus_points_list = []
    solid_defense_list = []
    creativity_list = []
    defense_errors_list = []
    goals_conceded_list = []
    goals_scored_list = []
    saves_list = []
    crosses_list = []
    threat_list = []
    ict_list = []
    minutes_list = []
    assists_list = []
    goals_involvement_list = []

    #Loop ends when index is 37, to exclude the last game of the season.
    while index < (rows):   
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

        if slice_df['minutes'].mean() > 0.0:
        
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
        
        index += 1

    points_list.append(None)
    points_per90_list.append(None)
    #chances_created_list.append(None)
    bonus_points_list.append(None)
    #solid_defense_list.append(None)
    creativity_list.append(None)
    #defense_errors_list.append(None)
    goals_conceded_list.append(None)
    goals_scored_list.append(None)
    saves_list.append(None)
    #crosses_list.append(None)
    threat_list.append(None)
    ict_list.append(None)
    minutes_list.append(None)
    assists_list.append(None)
    goals_involvement_list.append(None)

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
    ylabel_df = dataframe['goals_scored'] + dataframe['assists']

    dataframe['ylabel_1'] = ylabel_df.shift(-1)
    dataframe.dropna(inplace=True)

    #print(dataframe)
    return dataframe

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

#fname = "/home/zwi/zwi_work/Fantasy-Premier-League/data/2018-19/players/Adam_Lallana_250/gw.csv"
#create_model_features(fname)

#players_stats = pd.read_csv('pl_players_stats_detailed.csv')

#print(players_stats.columns)
#compute_seasons_rolling_stats(rootdir)


#########################################################################################################################################################################
#
#  Machine Learning Class definitions begin here
#
#########################################################################################################################################################################

class FPLSVMClassifier (svm.SVC):
    def obtain_training_data (self, cols, fname):
        "Function to load the training data for the ML model"
        df = pd.read_csv(fname)
        X_train = df.loc[:, cols]
        y_classifier = digitize_array(df.ylabel_1, 1)

        return X_train, y_classifier

    def fit_test_model (self, cols, fname):
        "Function to test the model on the data to be loaded."
        #Collecting the training data.
        training_xdata, training_ydata = self.obtain_training_data (cols, fname)

        self.fit(training_xdata, training_ydata)

        self.predict_proba([0, 0, 0, 0, 0])
    
    
