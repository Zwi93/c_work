import numpy as np 
from scipy.stats import norm

#New sigma and mu values for question 4(b) follow up question.
w = np.array([15, 125])
mean_w = np.mean(w)
std_w = np.std(w)


assets_mean = [0.0, (mean_w/100)/100]   # 1st entry for assets returns, 2nd for spreads.
assets_std = [0.03, (std_w/100)/100]

var_factor = -norm.ppf(0.01)  # Choose a positive z-score value.
portfolio_value = 40

def get_lvar (assets_mean, assets_std, var_factor, portfolio_value):

    lvar_1 = portfolio_value*(-assets_mean[0] + var_factor*assets_std[0])
    lvar_2 = portfolio_value*0.5*(assets_mean[1] + var_factor*assets_std[1]) 
    lvar = lvar_1 + lvar_2
    return lvar, lvar_1, lvar_2

lvar, lvar_1, lvar_2 = get_lvar(assets_mean, assets_std, var_factor, portfolio_value)

print('LVaR: ', lvar)
print('Normal VaR Attribution: ', lvar_1/lvar)
print('Spread-VaR Attribution: ', lvar_2/lvar)


