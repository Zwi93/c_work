from math import exp, sqrt
import random
import time
import numpy as np
import pandas as pd
from pandas.plotting import table
#from numba import jit
import matplotlib.pyplot as plt

spot_price = 100
strike = 100
rate = 0.1
vol = 0.2
random_walk_steps = 2000
simulations = 1000
expiry = 0.1

#@jit(nopython=True)
def random_walk_generator (spot_price, mu, vol, iteration_size, maturity):
    time_step = 0.0
    time_list = [time_step]
    price_list_norm = [spot_price]
    delta_t = maturity/iteration_size

    for i in range(1, iteration_size):
        time_step_i = time_step + i*delta_t
        time_list.append(time_step_i)
        random_value_norm = np.random.normal(0, 1)
        price_j = price_list_norm[-1]
        price_i = price_j*(1 + mu*delta_t + vol*random_value_norm*(sqrt(delta_t)))
        price_list_norm.append(price_i)

    return time_list, price_list_norm

def monte_carlo_estimate (spot_price, rate, vol, random_walk_steps, expiry, strike, no_of_simulation):

    estimate = 0

    for i in range(no_of_simulation):
        underlying_path = random_walk_generator(spot_price, rate, vol, random_walk_steps, expiry)[1]
        #payoff = max([(underlying_path[-1] - strike), 0])
        diff = abs((underlying_path[-1] - strike))
        payoff = max([(underlying_path[-1] - strike)/diff, 0])    #Payoff of a binary call option.
        estimate += payoff 

    estimate = estimate/no_of_simulation
    discounted_estimate = exp(-rate*expiry)*estimate

    return discounted_estimate

def plot_error_graph (filename):
    df = pd.read_csv(filename, delim_whitespace=True, names = ['Simulation', 'Mean', 'Std-Div'])
    simulations_list = df['Simulation']
    mean_list = df['Mean']
    std_div_list = df['Std-Div']

    fig = plt.figure(figsize=(20, 10))
    plt.ylim((0, 1))
    plt.xlim((990, 1200))
    plt.xlabel('No. of Simulations')
    plt.ylabel('Price')
    plt.title('Error Graphs for Monte Carlo Estimate')
    plt.errorbar(simulations_list, mean_list, yerr=std_div_list, marker='d', linestyle='')
    plt.hlines(0.532325, 990, 1200, colors='green')
    plt.show()


def plot_random_walks (spot_price, rate, vol, random_walk_steps, expiry, no_of_simulation):

    fig = plt.figure(figsize = (15, 10))

    time_list = random_walk_generator(spot_price, rate, vol, random_walk_steps, expiry)[0]

    for i in range(no_of_simulation):
        price_list_norm = random_walk_generator(spot_price, rate, vol, random_walk_steps, expiry)[1]
        plt.plot(time_list, price_list_norm)

    plt.show()

###############################################################################################################################################################

#Results from Computations.

t1 = time.clock()
call_option_price = monte_carlo_estimate(spot_price, rate, vol, random_walk_steps, expiry, strike, simulations)
#plot_random_walks(spot_price, rate, vol, random_walk_steps, expiry, simulations)
#plot_error_graph("stats.txt")
print("Monte Carlo Estimate: ", call_option_price)
t2 = time.clock()

print(t2 - t1)


