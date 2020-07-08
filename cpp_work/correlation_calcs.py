import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats, special
import matplotlib.pyplot as plt
from math import pow, sqrt

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


#Below is a function to fit a t copula by finding that mu that maximizes log-likelihood.
def log_lokelihood_mu (dataframe):

    #1st obtain the linearized, positive definite correlation matrix and its inverse and determinant.
    correlation_matrix = get_correlation(dataframe, "t_stat")
    inverse_correlation_matrix = np.linalg.inv(correlation_matrix)
    determinant = np.linalg.det(correlation_matrix)
    
    #Then the weekly data in uniform type, i.e in (0, 1).
    cds_historical_data_weekly = daily_to_weekly(dataframe)
    columns = cds_historical_data_weekly.columns.values.tolist()

    #Find the mu which maximizes the log-likelihood. 
    log_likelihood_dict = {}

    for mu in range(1, 25):
        
        log_likelihood = 0

        for i in range(cds_historical_data_weekly.shape[0]):

            implied_cdf_data = []  #this will contain data point for a single day in the historical data.

           #Select just one vector from this dictionary.
            for colmn in columns:
                implied_cdf = get_implied_cdf(cds_historical_data_weekly[colmn])[i]
                implied_cdf_data.append(implied_cdf)

            tcopula = multivariate_tcopula(implied_cdf_data, mu, inverse_correlation_matrix, determinant)
            log_likelihood += np.log10(tcopula)

        log_likelihood_dict[mu] = log_likelihood

    return log_likelihood_dict

    
    
#Below is a definition for the density function of the multivariate t copula.
def multivariate_tcopula (uniform_rvs, mu, inv_correlation_matrix, det_correlation_matrix):

    t_distributed_vector = [stats.t.ppf(a, mu) for a in uniform_rvs]
    t_distributed_vector = np.array(t_distributed_vector)
    triple_matrix_product = np.matmul(np.matmul(t_distributed_vector, inv_correlation_matrix), np.transpose(t_distributed_vector))
    numerator = pow(1 + triple_matrix_product/mu, -((mu + 5)/2))
    denominator = 1
    
    for i in range(len(uniform_rvs)):
        denominator *= pow((1 + pow(stats.t.ppf(uniform_rvs[i], mu), 2)), -((mu + 1)/2))

    power_term = pow(special.gamma(mu/2)/special.gamma((mu + 1)/2), 5)

    tcopula = (1/sqrt(abs(det_correlation_matrix)))*(special.gamma((mu + 5)/2)/special.gamma(mu/2))*power_term*numerator/denominator

    return tcopula

#Calculate the correlation matrix.
#correlation_matrix_gaussian = get_correlation(cds_historical_data_daily, "gaussian")
#correlation_matrix_t = get_correlation(cds_historical_data_daily, "t_stat")

#Write correlation matrix to .txt file.
#correlation_matrix_gaussian.to_csv("correlation_matrix_gaussian.txt", header=None, index=None, sep=" ", mode="w")
#correlation_matrix_t.to_csv("correlation_matrix_t.txt", header=None, index=None, sep=" ", mode="w")

#pfizer_cds_data = cds_historical_data_weekly['PFIZER']

#pfizer_implied_cdf = get_implied_cdf(pfizer_cds_data)

#print(pfizer_implied_cdf)

#fig = plt.figure(figsize=(15, 12))

#plt.scatter(np.arange(pfizer_cds_data.size), pfizer_cds_data)
#plt.plot(kde.support, kde.cdf, label="KDE")


log_likelihood_dict = log_lokelihood_mu(cds_historical_data_daily)
x_values = list(log_likelihood_dict.keys())
y_values = list(log_likelihood_dict.values())
plt.scatter(x_values, y_values)

plt.show()