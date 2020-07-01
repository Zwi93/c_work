//Include all relevant header files here.
#include <iostream>
#include <cmath>

using namespace std;

#define FREQUENCY 2

//Define a new type to hold data for a certain CDS/Bond contracts.
struct contract_info 
{
    string name;
    double price;
    double coupon;
    double maturity;
};

//Declare function prototypes here.
void bond_curve_bootstrapper (double zero_disc_factor[11]);
double bond_price_from_yield (double yield, double coupon_rate, double par_value, double bond_maturity);
void cds_curve_bootstrapper (double survival_probability[11], contract_info cds_info[6],double LGD);
double exponential_interpolation (double x_input, double a_param, double b_param, double fa_param, double fb_param);
struct contract_info *interpolate_par_curve (contract_info info_struct[6], int frequency);
void interpolate_par_curve1 (contract_info info_struct[6], contract_info interpolated_info[FREQUENCY*(6 - 1)]);
void get_hazard_rates (double survival_probability[11], double hazard_rates[11]);
double survival_time_inverse_cdf (double hazard_rates[11], double x_input);