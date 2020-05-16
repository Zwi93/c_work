from random import uniform, normalvariate
from math import exp

def monte_carlo_estimate (no_of_trials):

    estimate = 0
    for i in range(no_of_trials):

        uniform_random = uniform(0, 1)
        estimate += exp(uniform_random)

    return estimate/no_of_trials

estimate = monte_carlo_estimate(1000000)

exact = exp(1) - exp(0)

print("Estimate: ", estimate)
print("Exact: ", exact)
