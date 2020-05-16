/* Module for the construction of the binomial option price model. */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define SPOT_PRICE 100
#define STRIKE 100
#define EXPIRY 1.0
#define RATE 0.05
#define VOLATILITY 0.2
#define STEPS 1000

#define TIME_STEP EXPIRY/STEPS

void generate_binomial_tree (double *array, double spot_price, int no_of_steps, double up_factor, double down_factor);
void generate_payoff_array (double *asset_array, double *payoff_array , double strike, int no_of_steps);
double vanilla_payoff_function (double stock_price, double strike, char type);
double get_binomial_price ();
double black_scholes_price (double spot_price, double strike, double expiry, double rate, double vol, double dividend_yield);
double normal_cdf (double x_param);
double binary_payoff_function (double stock_price, double strike, char type);
double binary_option_price (double spot_price, double strike, double expiry, double rate, double vol);
double forward_payoff_function (double stock_price, double spot_price, double rate, double expiry);
void execute_binomial_pricing (double spot_price, double strike, double expiry, double rate, double vol, int asset_steps, double delta_t);

int main ()
{
    execute_binomial_pricing (SPOT_PRICE, STRIKE, EXPIRY, RATE, VOLATILITY, STEPS, TIME_STEP);    

    return 0;
}

void execute_binomial_pricing (double spot_price, double strike, double expiry, double rate, double vol, int asset_steps, double delta_t)
{
    double asset_array[asset_steps];
    double payoff_array[asset_steps];
    
    //Compute neccessary parameters for use in asset price tree generation.
    double disc_fct = exp(-rate*delta_t); 
    double temp1 = exp((rate + vol*vol)*delta_t);
    double temp2 = 0.5*(disc_fct + temp1);
    double up_factor = temp2 + sqrt(temp2*temp2 - 1);
    double down_factor = 1/up_factor;
    double risk_neut_prob = (exp(rate*delta_t) - down_factor)/(up_factor - down_factor);
    double option_price_binomial, option_price_bs;

    //Populate the asset array with binomial model data.
    generate_binomial_tree(asset_array, spot_price, asset_steps, up_factor, down_factor);
    generate_payoff_array(asset_array, payoff_array, strike, asset_steps);

    option_price_binomial = get_binomial_price(payoff_array, asset_steps, risk_neut_prob, disc_fct);
    option_price_bs = binary_option_price(spot_price, strike, expiry, rate, vol);

    printf("Binomial price: %f\n", option_price_binomial);
    printf("Black Scholes price: %f\n", option_price_bs);
}

void generate_binomial_tree (double *asset_array, double spot_price, int no_of_steps, double up_factor, double down_factor)
{
    int index;
    asset_array[0] = spot_price;

    for (index = 1; index < no_of_steps; index++)
    {
        int inner_index;
        for (inner_index = index; inner_index > 0; inner_index--)
        {
            asset_array[inner_index] = up_factor*asset_array[inner_index - 1];
        }

        asset_array[0] = down_factor*asset_array[0];
    } 
}

void generate_payoff_array (double *asset_array, double *payoff_array , double strike, int no_of_steps)
{
    int index;
    for (index = 0; index <= no_of_steps; index++)
    {
        //payoff_array[index] = binary_payoff_function(asset_array[index], strike, 'C');
        payoff_array[index] = forward_payoff_function(asset_array[index], strike, RATE, EXPIRY);
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

double binary_payoff_function (double stock_price, double strike, char type)
{
    double payoff;
    switch (type)
    {
    case 'C':
 
        if (stock_price - strike > 0)
        {
            payoff = 1.0;
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
            payoff = 1.0;
        }
        return payoff;
        break;

    default:
        break;
    }
}

double get_binomial_price (double *payoff_array, int no_of_steps, double risk_neut_prob, double disc_fct)
{
    int index;
    for (index = no_of_steps - 1; index >= 0; index--)
    {
        int inner_index;
        for (inner_index = 0; inner_index < no_of_steps; inner_index++)
        {
            payoff_array[inner_index] = (risk_neut_prob*payoff_array[inner_index + 1] + (1 - risk_neut_prob)*payoff_array[inner_index])*disc_fct;
        }
    } 
    return payoff_array[0];
}

double normal_cdf (double x_param)
{
    double normal_cdf;
    double new_param = x_param/sqrt(2);

    normal_cdf = 0.5 + 0.5*erf(new_param);

    return normal_cdf;
}

double black_scholes_price (double spot_price, double strike, double expiry, double rate, double vol, double dividend_yield)
{
    //Function to compute the vanilla call option price.
    double d1, d2;
    d1 = (log(spot_price/strike) + (rate - dividend_yield + 0.5*vol*vol)*expiry)/(vol*sqrt(expiry));
    d2 = d1 - vol*sqrt(expiry);

    //Compute the Black-Scholes price for a call. 
    double bs_price;
    bs_price = spot_price*exp(-dividend_yield*expiry)*normal_cdf(d1) - strike*exp(-rate*expiry)*normal_cdf(d2);

    return bs_price;   
}

double binary_option_price (double spot_price, double strike, double expiry, double rate, double vol)
{
    //Function to calculate the price of a binary call option.
    double d1, d2;
    d1 = (log(spot_price/strike) + (rate + 0.5*vol*vol)*expiry)/(vol*sqrt(expiry));
    d2 = d1 - vol*sqrt(expiry);

    double binary_price;
    binary_price = exp(-rate*expiry)*normal_cdf(d2);

    return binary_price;    
}

double forward_payoff_function (double stock_price, double spot_price, double rate, double expiry)
{
    double delivery_price, payoff;

    delivery_price = spot_price*exp(rate*expiry);
    payoff = stock_price - delivery_price;

    return payoff;
}