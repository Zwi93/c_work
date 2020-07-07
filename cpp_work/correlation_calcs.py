import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt


#Read in cds data from excel file.
cds_historical_data_daily = pd.read_excel("cds_data.xlsx", names = ["DATE", "PFIZER", "MSI", "HPQ", "FCO", "CAT"])

#Convert the daily data into weekly and remove the date column.
def daily_to_weekly (dataframe):
    rows = dataframe.shape[0]
    columns = dataframe.shape[1]

    weekly_data_array = np.zeros((rows, columns - 1))

    for i in range(0, rows, 5):
        weekly_data_array[int(i/5)] = dataframe[["PFIZER", "MSI", "HPQ", "FCO", "CAT"]].iloc[i]

    weekly_data_df = pd.DataFrame(weekly_data_array, columns = ["PFIZER", "MSI", "HPQ", "FCO", "CAT"])
    
    #Remove zeros from the dataframe.
    weekly_data_df = weekly_data_df.loc[(weekly_data_df != 0).any(axis=1)]

    return weekly_data_df

#Define the CDF for the data.
def get_implied_cdf (the_array):
    
    #Perform KDE to estimate cdf. 
    kde = sm.nonparametric.KDEUnivariate(the_array)
    kde.fit()
    support_cdf = kde.cdf
    support_interval = kde.support[2] - kde.support[1]

    implied_cdf = np.zeros(the_array.shape[0])
    running_index = 0
    for element in the_array:

        index = (element - kde.support[0])/support_interval
        index = int(index)
        implied_cdf[running_index] = support_cdf[index]

        running_index += 1 

    return implied_cdf


#Define function to compute the correlation depending on the copula type.
def get_correlation (dataframe, copula_type):

    #First get the weekly data from the raw dataframe.
    cds_historical_data_weekly = daily_to_weekly(dataframe)
    columns = cds_historical_data_weekly.columns.values.tolist()
    implied_dict = {}

    #Perform transformation of the raw data into uniform and normal RVs.
    for column in columns:
        if copula_type is "gaussian":
            implied_cdf = get_implied_cdf(cds_historical_data_weekly[column])
            implied_normal_rvs = stats.norm.ppf(implied_cdf)
            implied_dict[column] = implied_normal_rvs
        elif copula_type is "t_stat":
            implied_cdf = get_implied_cdf(cds_historical_data_weekly[column])
            implied_dict[column] = implied_cdf
        else:
            implied_dict[columns] = np.zeros(cds_historical_data_weekly.shape[0])
        
    #Create dataframe of this and compute the correlation after while handling the two cases of copula type.
    if copula_type is "gaussian":
        transformed_dataframe = pd.DataFrame(implied_dict)
        correlation_matrix = transformed_dataframe.corr()
        return correlation_matrix
    elif copula_type is "t_stat":
        #Define function to transform rank matrix to almost linear matrix.
        def linearize_correlation_matrix (a):
            return 2*np.sin(3.14*a/6)

        transformed_dataframe = pd.DataFrame(implied_dict)
        correlation_matrix = transformed_dataframe.corr()

        #Linearise the rank matrix obtained.
        linearized_correlation_matrix = correlation_matrix.applymap(linearize_correlation_matrix)

        #Convert diagonals to 1.
        factor = linearized_correlation_matrix.iloc[0][0]
        linearized_correlation_matrix = linearized_correlation_matrix.applymap(lambda x: x/factor)

        #Compute eigenvalue decomposition.
        eigen_values, right_eigenvectors  = np.linalg.eig(linearized_correlation_matrix)

        return linearized_correlation_matrix


#Calculate the correlation matrix.
correlation_matrix_gaussian = get_correlation(cds_historical_data_daily, "gaussian")
correlation_matrix_t = get_correlation(cds_historical_data_daily, "t_stat")

#Write correlation matrix to .txt file.
correlation_matrix_gaussian.to_csv("correlation_matrix_gaussian.txt", header=None, index=None, sep=" ", mode="w")
correlation_matrix_t.to_csv("correlation_matrix_t.txt", header=None, index=None, sep=" ", mode="w")

#pfizer_cds_data = cds_historical_data_weekly['PFIZER']

#pfizer_implied_cdf = get_implied_cdf(pfizer_cds_data)

#print(pfizer_implied_cdf)

#fig = plt.figure(figsize=(15, 12))

#plt.scatter(np.arange(pfizer_cds_data.size), pfizer_cds_data)
#plt.plot(kde.support, kde.cdf, label="KDE")

#plt.show()