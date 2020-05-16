import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from pandas.plotting import register_matplotlib_converters
from math import log, sqrt
from scipy.stats import norm

register_matplotlib_converters()

df = pd.read_csv('SP500.csv')
historical_data = np.array(df)
del df # free up memory.

dates_list_0 = historical_data[:, 0]
price_list = historical_data[:, 1]

#Obtain the appropriate factor from the inverse cdf for the normal distribution function assuming 99% confidence level.
var_factor = norm.ppf(0.01)
sample_size = 21

def get_log_returns (price_list, sample_size):

    #Create log returns list and update dates array since 1st day doesn't have a log return.
    price_ratio_list = price_list[1:]/price_list[: -1]
    log_returns_list = [log(elememt) for elememt in price_ratio_list] 
    log_returns_list = np.array(log_returns_list)

    #Obtain 10 days log-returns. 1st translate the price array sample-size days ahead.
    translated_price_list = price_list[sample_size:]
    ten_day_log_returns_0 = translated_price_list[10:]/translated_price_list[:-10]
    ten_day_log_returns = [log(elememt) for elememt in ten_day_log_returns_0]
    ten_day_log_returns = np.array(ten_day_log_returns)

    return log_returns_list, ten_day_log_returns

def do_backtest_var (log_returns_list, var_factor, sample_size, sigma_type):

    #Determine eligible number of observation.
    size_of_data = log_returns_list.size
    no_of_observation = size_of_data - sample_size
    
    #Construct 21 days roling window var; standard deviation. And corresponding 10 day 99% VaR.
    var_10_day_array = np.zeros(no_of_observation)
    vol_estimates = np.zeros(no_of_observation + 1)
    initial_vol = np.std(log_returns_list[:sample_size])  # Initial estimate for vol; needed for EWMA method.
    vol_estimates[0] = initial_vol

    for i in range(no_of_observation):

        #Catering for the two cases of normal or EWMA volatility.
        if sigma_type is "NORMAL":
            sample_array = log_returns_list[i: i + sample_size]
            std_sample_array = np.std(sample_array)
            var_10_day = var_factor*std_sample_array*sqrt(10)

        elif sigma_type is "EWMA":
            lambda_1 = 0.72
            prior_vol_estimate = vol_estimates[i]
            latest_return_data = log_returns_list[i + sample_size]
            ith_variance_estimate = lambda_1*prior_vol_estimate**(2) + (1 - lambda_1)*latest_return_data**(2)
            ith_vol_estimate = sqrt(ith_variance_estimate)
            var_10_day = var_factor*ith_vol_estimate*sqrt(10)
            vol_estimates[i + 1] = ith_vol_estimate  # Update the list of estimates.

        var_10_day_array[i] = var_10_day

    return var_10_day_array

def do_backtest_analysis (var_10_day_array, ten_day_log_returns):

    #Compute the difference of the var 10 day array with ten day log-return.
    #1st equate the sizes of the arrays.
    size_of_observation = min(ten_day_log_returns.size, var_10_day_array.size)
    var_log_difference = ten_day_log_returns - var_10_day_array[:size_of_observation]

    #Get the indices where there is a breach in VaR.
    var_breach_condition = np.where(var_log_difference < 0)[0]
    number_of_breaches = var_breach_condition.size 
    percentage_breach = number_of_breaches/size_of_observation

    #Check for consecutive breaches; ones occuring at indices i, and i + 1.
    consecutive_breach_condition0 = var_breach_condition[1:] - var_breach_condition[:-1] # This gives 1 for each consecutive breaches.
    consecutive_breach_condition = np.where(consecutive_breach_condition0 == 1)[0]
    number_consec_breaches = consecutive_breach_condition.size

    return percentage_breach, number_consec_breaches



log_returns_list, ten_day_log_returns = get_log_returns(price_list, sample_size) 
var_10_day_array = do_backtest_var(log_returns_list, var_factor, sample_size, "NORMAL")  # NORMAL or EWMA determine which volatility method to use.

print("% of breaches: ", do_backtest_analysis(var_10_day_array, ten_day_log_returns)[0])
print("Number of consecutive breaches: ", do_backtest_analysis(var_10_day_array, ten_day_log_returns)[1])

#Plotting the backtest VaR time series. 
fig = fig = plt.figure(figsize=(15, 20))
size_of_plot = min(ten_day_log_returns.size, var_10_day_array.size)
#dates_list = dates_list_0[1 + sample_size:size_of_plot]
x_data = np.arange(size_of_plot)

plt.title('Backtest results: Standard volatility Method')
plt.ylabel('Returns')
plt.xlabel('No. of days')
plt.plot(x_data, ten_day_log_returns, '-', ms=1, label='10D log-returns', color='green')
plt.plot(x_data, var_10_day_array[:size_of_plot], '-', ms=0.1, label='10D 99% VaR', color='blue')
plt.legend()
plt.show()