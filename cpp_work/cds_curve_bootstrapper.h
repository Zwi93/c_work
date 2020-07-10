//Include all relevant header files here.
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>

using namespace std;

//Declare important macros here.
#define FREQUENCY 2
#define No_COMPANIES 5 //number of underlyings in the basket.
#define SIMULATIONS 5
#define NATURAL_EXP exp(1)
#define MY_PI 4*atan(1.0)  //pi to be used only in this script.
#define MATURITY 1.0

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
void interpolate_par_curve1 (contract_info info_struct[6], contract_info interpolated_info[FREQUENCY*(6 - 1)]);
void get_hazard_rates (double survival_probability[11], double hazard_rates[11]);
double survival_time_inverse_cdf (double hazard_rates[11], double x_input, int divisions, double accuracy_level);
double survival_time_inverse_cdf1 (double hazard_rates[11], double x_input, double time_interval);
//struct contract_info *interpolate_par_curve (contract_info info_struct[6], int frequency);
void get_pseudo_square_root (double correlation_matrix[][No_COMPANIES], double pseudo_matrix[][No_COMPANIES]);
double normal_cdf (double x_param);
double inverse_error_function (int order, double x_param);
double inverse_normal_cdf (int order, double x_param);
double factorial_of_x (int x_param);
double beta_function (double a_param, double b_param);
double student_t_cdf (double x_value, double mu);
long double incomplete_beta_function (double a_param, double b_param, double x_variable);
double incomplete_beta_function1 (double a_param, double b_param, double x_variable);
long double hypergeometric_function (int order, double a_param, double b_param, double c_param, double x_variable);
void get_correlation_matrix (double correlation_array[][No_COMPANIES], string copula_type);
void one_to_many_dimension (double one_dimension_array[No_COMPANIES], double many_dimension_array[][No_COMPANIES]);
void matrix_product (double array_one[][No_COMPANIES], double array_two[][No_COMPANIES], double product_array[][No_COMPANIES], double scale_factor);
double inverse_error_function1 (double x_param);
void basket_cds_mc_pricing_adjusted (int no_of_credits, int no_of_simulations, int order, contract_info cds_curves_matrix[No_COMPANIES][6], double LGD, int nth_default, double maturity, string copula_type);
void basket_cds_mc_pricing (int no_of_credits, int no_of_simulations, int order, contract_info cds_curves_matrix[No_COMPANIES][6], double LGD, int nth_default, double maturity, string copula_type);
double get_minimum_value (double array[No_COMPANIES]);
double get_nth_minimum_value (double array[No_COMPANIES], int n);
double premium_protection_leg_calcs (double nth_default_time, double maturity, double LGD, double delta_t, double zero_disc_factor[11], double payoff_legs[2]);
double f(double x, double a, double b);
double simpson(double lower_bound, double upper_bound, double no_steps, double a, double b);
double trapezoidal (double lower_bound, double upper_bound, double no_steps, double a, double b);