import matplotlib.pyplot as plt
import numpy as np 
import random 

#Model inputs.
assets_mean = np.array([0.02, 0.07, 0.15, 0.2])
assets_var = np.array([0.05, 0.12, 0.17, 0.25])
correlation_matrix = np.array([[1, 0.3, 0.3, 0.3], [0.3, 1, 0.6, 0.6], [0.3, 0.6, 1, 0.6], [0.3, 0.6, 0.6, 1]])

##########################################################################################################################################################
#Definitions of functions.

def get_covariance_from_correlation (correlation_matrix, assets_var, multiplier):

    zeros_matrix = np.zeros((4, 4))

    #Change the diagonal zeros to assets sigmas.
    for i in range(4):
        zeros_matrix[i][i] = assets_var[i]

    #Get covariance matrix from correlation matrix.
    correlation_matrix = multiplier*correlation_matrix
    covariance_matrix = np.linalg.multi_dot([zeros_matrix, correlation_matrix, zeros_matrix])

    return covariance_matrix

def get_opportunity_set (assets_mean, assets_var, covariance_matrix, trials):

    mean_list = []
    var_list = []
    weights_range = np.arange(-trials, trials) # List of integers in the range (-trials, trials).

    for i in range(trials): 

        #Choose random integers in the sample weights_range = (-trials, trials).
        w1 = random.choice(weights_range)/100
        w2 = random.choice(weights_range)/100
        w3 = random.choice(weights_range)/100
        w4 = 1 - (w1 + w2 + w3)
        weight_vector = np.array([w1, w2, w3, w4])
        mean_port, risk_port = get_port_risk_return(assets_mean, weight_vector, covariance_matrix)
        mean_list.append(mean_port)
        var_list.append(risk_port)

    return mean_list, var_list
    
def get_minimum_variance_weights (assets_mean, assets_var, covariance_matrix, target_return):
    
    #Obtain the 4 numbers to solve for lagrange multipliers.
    ones_array = np.ones(4)
    inverse_covariance_matrix = np.linalg.inv(covariance_matrix)
    a1 = np.linalg.multi_dot([ones_array, inverse_covariance_matrix, ones_array])
    a2 = np.linalg.multi_dot([ones_array, inverse_covariance_matrix, assets_mean])
    b1 = np.linalg.multi_dot([assets_mean, inverse_covariance_matrix, ones_array])
    b2 = np.linalg.multi_dot([assets_mean, inverse_covariance_matrix, assets_mean])

    #Create matrix relevant to solve for the lagrange multipliers.
    lagrange_matrix = np.array([[a1, a2], [b1, b2]])
    inverse_lagrange_matrix = np.linalg.inv(lagrange_matrix)
    lagrange_vector = np.linalg.multi_dot([inverse_lagrange_matrix, np.array([-1, -target_return])])

    #These are the two lagrange multipliers.
    lagrange_multiplier1 = lagrange_vector[0]
    lagrange_multiplier2 = lagrange_vector[1]

    #Solve for the minimum variance given the target return.
    lagrange_terms = ones_array*lagrange_multiplier1 + assets_mean*lagrange_multiplier2  # This is a vector.
    minimum_var_weights = (-1)*np.linalg.multi_dot([inverse_covariance_matrix, lagrange_terms])

    return minimum_var_weights

def get_tangency_portfolio (assets_mean, assets_var, covariance_matrix, risk_free_rate):

    ones_array = np.ones(4)
    inverse_covariance_matrix = np.linalg.inv(covariance_matrix)

    #Computute factors neccesarry for calculation of weights of tangency portfolio.
    mean_risk_free_vector = assets_mean - ones_array*risk_free_rate
    numerator_factor = np.linalg.multi_dot([inverse_covariance_matrix, mean_risk_free_vector])  # This is a vector.
    denominator_factor = np.linalg.multi_dot([ones_array, inverse_covariance_matrix, mean_risk_free_vector]) 

    #Then compute the weights of the tangency portfolio.
    tangency_port_weights = numerator_factor/denominator_factor

    return tangency_port_weights

def get_port_risk_return (assets_mean, weight_vector, covariance_matrix):

    #Obtain the risk and return for a porfolio given the weights, covariance-matrix and means of each asset.
    mean_port = np.dot(weight_vector, assets_mean)
    var_port_squared = np.linalg.multi_dot([weight_vector, covariance_matrix, weight_vector])
    risk_port = var_port_squared**(0.5)

    return mean_port, risk_port

def get_true_eff_frontier (assets_mean, tangency_port_weights, covariance_matrix, risk_free_rate):

    #Get the associated two (risk, return) pairs to be able to plot the efficient frontier line.
    tangency_port_mean, tangency_port_risk = get_port_risk_return(assets_mean, tangency_port_weights, covariance_matrix)

    plt.plot([0, tangency_port_risk], [risk_free_rate, tangency_port_mean])

##############################################################################################################################################################
#Results from the model

fig = plt.figure(figsize = (15, 10))

#3 cases for different Stress Factors on the Correlation matrix.
covariance_matrix1 = get_covariance_from_correlation(correlation_matrix, assets_var, 1)
covariance_matrix2 = get_covariance_from_correlation(correlation_matrix, assets_var, 1.25)
covariance_matrix3 = get_covariance_from_correlation(correlation_matrix, assets_var, 1.5)

minumum_var_weights1 = get_minimum_variance_weights(assets_mean, assets_var, covariance_matrix1, 0.045)
minumum_var_weights2 = get_minimum_variance_weights(assets_mean, assets_var, covariance_matrix2, 0.045)
minumum_var_weights3 = get_minimum_variance_weights(assets_mean, assets_var, covariance_matrix3, 0.045)

print('Minimum Var weights factor 1: ', minumum_var_weights1)
print('Associated risk: ', get_port_risk_return(assets_mean, minumum_var_weights1, covariance_matrix1)[1])
print('Minimum Var weights factor 1.25: ', minumum_var_weights2)
print('Associated risk: ', get_port_risk_return(assets_mean, minumum_var_weights2, covariance_matrix2)[1])
print('Minimum Var weights factor 1.5: ', minumum_var_weights3)
print('Associated risk: ', get_port_risk_return(assets_mean, minumum_var_weights3, covariance_matrix3)[1])

#4 cases for the risk-free rate.
tangency_port_weights1 = get_tangency_portfolio(assets_mean, assets_var, covariance_matrix1, 0.5/100)
tangency_port_weights2 = get_tangency_portfolio(assets_mean, assets_var, covariance_matrix1, 1./100)
tangency_port_weights3 = get_tangency_portfolio(assets_mean, assets_var, covariance_matrix1, 1.5/100)
tangency_port_weights4 = get_tangency_portfolio(assets_mean, assets_var, covariance_matrix1, 1.75/100)

print('Tangency Portfolio weights for given 50bps rate: ', tangency_port_weights1)
print('Associated risk: ', get_port_risk_return(assets_mean, tangency_port_weights1, covariance_matrix1)[1])
print('Tangency Portfolio weights for given 100bps rate: ', tangency_port_weights2)
print('Associated risk: ', get_port_risk_return(assets_mean, tangency_port_weights2, covariance_matrix1)[1])
print('Tangency Portfolio weights for given 150bps rate: ', tangency_port_weights3)
print('Associated risk: ', get_port_risk_return(assets_mean, tangency_port_weights3, covariance_matrix1)[1])
print('Tangency Portfolio weights for given 175bps rate: ', tangency_port_weights4)
print('Associated risk: ', get_port_risk_return(assets_mean, tangency_port_weights4, covariance_matrix1)[1])

#Plotting of relevant graphs.
get_true_eff_frontier(assets_mean, tangency_port_weights2, covariance_matrix1, 1/100)
get_true_eff_frontier(assets_mean, tangency_port_weights4, covariance_matrix1, 1.75/100)
 
mean_list, sigma_list = get_opportunity_set(assets_mean, assets_var, covariance_matrix1, 5000)
plt.plot(sigma_list, mean_list, '.', ms=2)

plt.show()
