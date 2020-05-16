/* Script to implement the explicit finite difference method in C */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define STRIKE 100
#define RATE 0.05
#define VOLATILITY 0.2
#define EXPIRY 1.0
#define ASSET_BOUND 2*STRIKE
#define ASSET_STEPS 20
#define DELTA_ASSET ASSET_BOUND/ASSET_STEPS

void explicit_fdm_option_estimates (double array[][ASSET_STEPS], double vol, double rate, double strike, double delta_s, double delta_t, int asset_steps, int time_steps);
double vanilla_payoff_function (double stock_price, double strike, char type);

int main ()
{
    //Stability condition; delta_t has to equal this value.
    double delta_t = 1/(pow(VOLATILITY, 2)*pow(ASSET_STEPS, 2));
    int time_steps = (int) EXPIRY/delta_t + 1;
    delta_t = EXPIRY/time_steps;
    
    double option_values[time_steps][ASSET_STEPS];

    explicit_fdm_option_estimates(option_values, VOLATILITY, RATE, STRIKE, DELTA_ASSET, delta_t, ASSET_STEPS, time_steps);

    int index;

    for (index = 0; index < ASSET_STEPS; index++)
    {
        printf("%lf\n", option_values[0][index]);
    }

    return 0;
}

void explicit_fdm_option_estimates (double array[][ASSET_STEPS], double vol, double rate, double strike, double delta_s, double delta_t, int asset_steps, int time_steps)
{
    //Function to implement the explicit finite difference method for option pricing.

    int time_index, asset_index;

    for (asset_index = 0; asset_index < asset_steps; asset_index++)
    {
        array[0][asset_index] = vanilla_payoff_function(asset_index*delta_s, strike, 'C');
    }

    for (time_index = 1; time_index < (time_steps); time_index++)
    {
        for (asset_index = 1; asset_index < (asset_steps - 1); asset_index++)
        {
            double delta, gamma, theta;

            delta = (array[time_index - 1][asset_index + 1] - array[time_index - 1][asset_index - 1])/(2*delta_s);
            gamma = (array[time_index - 1][asset_index + 1] -2*array[time_index - 1][asset_index] + array[time_index - 1][asset_index - 1])/(pow(delta_s, 2));
            theta = -0.5*pow(vol, 2)*pow(asset_index*delta_s, 2)*gamma - rate*(asset_index*delta_s)*delta + rate*array[time_index - 1][asset_index];
            
            array[time_index][asset_index] = array[time_index - 1][asset_index] - delta_t*theta;
        }
    
        array[time_index][0] = array[time_index - 1][0]*(1 - rate*delta_t);
        array[time_index][asset_steps - 1] = 2*array[time_index][asset_steps - 2] - array[time_index][asset_steps - 3]; 
    }
}

double vanilla_payoff_function (double stock_price, double strike, char type)
{
    double payoff;
    switch (type)
    {
    case 'C':
   
        if (stock_price - strike > 0)
        {
            payoff = stock_price - strike;
        }
        else
        {
            payoff = 0.0;
        }
        return payoff;
        break;

    case 'P':

        if (stock_price - strike > 0)
        {
            payoff = 0.0;
        }
        else
        {
            payoff = strike - stock_price;
        }
        return payoff;
        break;

    default:
        break;
    }
}