/************************************************************************************************************************************
 * Purpose: Basic CDS curve bootstrapper. Script takes the CDS curve and calculates the risk-neutral survival probabilities.        * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Usage: Run the program and it will print out the bootstrapped survival probabilities.                                            *
 *                                                                                                                                  *
 ************************************************************************************************************************************
 */

//Include all relevant header files here.
#include <iostream>
#include <cmath>
using namespace std;

//Declare function prototypes here.
void bond_curve_bootstrapper (double zero_disc_factor[11]);
double bond_price_from_yield (double yield, double coupon_rate, double par_value, int bond_maturity);
void cds_curve_bootstrapper (double survival_probability[6], double LGD);
double exponential_interpolation (double x_input, double a_param, double b_param, double fa_param, double fb_param);

//Define a new type to hold data for a certain CDS contract.
struct cds_contract 
{
    string cds_name;
    double cds_spread;
    double cds_maturity;
};

// define struct type to hold info about bonds.
struct coupon_bonds 
{
    string bond_name;
    float yield;
    float coupon;
    float maturity;
};

int main ()
{
    //Obtain the bootstrapped zero yields from bonds' prices.
    double risk_free_df[11];  //Array to store the bootstrapped zero discount factors.
    bond_curve_bootstrapper(risk_free_df); //function to bootstrapp bond curve.

    //Initiate input variables.
    double survival_probability[6];
    double LGD = 0.4;

    //Bootstrapp cds curve.
    //cds_curve_bootstrapper(survival_probability, LGD);

    return 0;
}

/************************************************************************************************************************************
 * Purpose: Function to bootstrapp the cds curve from given input data.                                                             * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * survival-probability: Array to store the implied survival probabilities from the bootstrapp.                                     *
 * LGD : Loss given default value                                                                                                   *
 * Return: This is a void function.                                                                                                 *                                                                                                                                  
 ************************************************************************************************************************************
 */
void cds_curve_bootstrapper (double survival_probability[6], double LGD = 0.4)
{
    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_contract cds_info[5];
    cds_info[0] = {"1Y cds", 100, 1.0};
    cds_info[1] = {"2Y cds", 114.00, 2.0};
    cds_info[2] = {"3Y cds", 121.0, 3};
    cds_info[3] = {"4Y cds", 135.0, 4};
    cds_info[4] = {"5Y cds", 145.0, 5.0};

    //Obtain the bootstrapped zero yields from bonds' prices.
    double risk_free_df[6];  //Array to store the bootstrapped zero discount factors.
    bond_curve_bootstrapper(risk_free_df); //function to bootstrapp bond curve.

    //Initialize useful variable.
    int index;

    //Initialize array with 1s.
    for (index = 0; index < 6; index++)
    {
        survival_probability[index] = 1.0;
    }

    //Begin bootstrapping here.
    //First calculate the 1st implied survival probability.
    survival_probability[1] = LGD/(LGD + cds_info[0].cds_spread/pow(10, 4));

    //Then calculate the 2nd, 3rd etc...
    for (index = 2; index < 6; index++)
    {
        double temp_calc = 0;  //Variable to store summation. Only needed in this scope.
        int inner_index;

        for (inner_index = 1; inner_index < index; inner_index++)
        {
            temp_calc += risk_free_df[inner_index]*(LGD*survival_probability[inner_index - 1] - (LGD + cds_info[index - 1].cds_spread/pow(10, 4))*survival_probability[inner_index]);
        }

        //spreads are divived by 10^4 for conversion to %.
        survival_probability[index] = temp_calc/(risk_free_df[index]*(LGD + cds_info[index - 1].cds_spread/pow(10, 4))) + survival_probability[index - 1]*LGD/(LGD + cds_info[index - 1].cds_spread/pow(10, 4)); 
    }

    //Print out the results.
    for (index = 1; index < 6; index++)
    {
        cout << cds_info[index - 1].cds_name + " survival probability\n" << survival_probability[index] << endl;
    }
}

/************************************************************************************************************************************
 * Purpose: Function to bootstrapp the cds curve from given input data.                                                             * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * zero_disc_factor: 1d array to store discount factors; passed as reference parameter.                                             *
 *                                                                                                                                  *
 * Return: This is a void function.                                                                                                 *                                                                                                                                  
 ************************************************************************************************************************************
 */
void bond_curve_bootstrapper (double zero_disc_factor[11])
{
    // Create array to carry the information of bonds to be bootstrapped. Data taken on 2020/06/26.
    coupon_bonds bonds_info[6];
    bonds_info[0] = {"0.5Y bond", 0.00167, 0.0, 0.5};
    bonds_info[1] = {"1Y bond", 0.00162, 0.0, 1.0};
    bonds_info[2] = {"2Y bond", 0.00168, 0.0013, 2.0};
    bonds_info[3] = {"3Y bond", 0.00186, 0.0013, 3};
    bonds_info[4] = {"4Y bond", 0.00236, 0.0015, 4};  //Interpolated.
    bonds_info[5] = {"5Y bond", 0.003, 0.0025, 5.0};

    //Initialize useful variable.
    int index, running_index = 0;

    //Interpolate yields.
    coupon_bonds interpolated_bonds_info[10];

    interpolated_bonds_info[0] = bonds_info[0];

    for (index = 1; index < 5; index++)
    {
        running_index += 1;
        interpolated_bonds_info[running_index] = bonds_info[index];
        double a_param, b_param, fa_param, fb_param;
        a_param = bonds_info[index].maturity;
        b_param = bonds_info[index + 1].maturity;
        fa_param = bonds_info[index].yield;
        fb_param = bonds_info[index + 1].yield;

        running_index += 1;
        interpolated_bonds_info[running_index].bond_name = to_string(a_param + 0.5) + "Y bond";
        interpolated_bonds_info[running_index].coupon = bonds_info[index + 1].coupon;
        interpolated_bonds_info[running_index].maturity = a_param + 0.5; 
        interpolated_bonds_info[running_index].yield = exponential_interpolation(a_param + 0.5, a_param, b_param, fa_param, fb_param);
    }

    interpolated_bonds_info[9] = bonds_info[5];

    //Initialize element 0 for zero_disc_factor array.
    zero_disc_factor[0] = 0.0;

    //Begin the bootstrapp here.
    for (index = 1; index < 11; index++)
    {
        double current_bond_price = bond_price_from_yield(interpolated_bonds_info[index - 1].yield, interpolated_bonds_info[index - 1].coupon, 1.0, interpolated_bonds_info[index - 1].maturity);
        double temp_factor = 0;

        cout << interpolated_bonds_info[index - 1].bond_name + " price\n";
        cout << current_bond_price << endl; 

        int inner_index;
        for (inner_index = 0; inner_index < index; inner_index++)
        {
            temp_factor += zero_disc_factor[inner_index]*interpolated_bonds_info[inner_index].coupon;
        }

        zero_disc_factor[index] = (current_bond_price - temp_factor)/(interpolated_bonds_info[index - 1].coupon + 1);  //Face value is one for now.
    }
    cout << endl;

    for (index = 1; index < 11; index++)
    {
        cout << interpolated_bonds_info[index - 1].bond_name + " zero factor\n" << zero_disc_factor[index] << endl;
    }
}

double bond_price_from_yield (double yield, double coupon_rate, double par_value, int bond_maturity)
{
/*
Function to compute the price of a bond given its yield, coupon rate, and maturity. Zero coupons bonds are special cases of these.
*/
    int index;
    double bond_value = 0.0;
    double coupon_date = 0.0;

    for (index = 1; index <= bond_maturity; index++)
    {
        coupon_date = index; 
        bond_value += coupon_rate*exp(-yield*coupon_date);
    }

    bond_value += par_value*exp(-yield*bond_maturity);
    
    return bond_value; 
}

double exponential_interpolation (double x_input, double a_param, double b_param, double fa_param, double fb_param)
{
    double fx_value; // Interpolated value at x_input.
    double exponent_value;  //Intermediate value going into the exponent.

    //Compute the interpolation using exponential and logs.
    if (x_input < b_param & x_input > a_param)
    {
        exponent_value = log(fa_param) + log(fb_param/fa_param)*(x_input - a_param)/(b_param - a_param);
        fx_value = exp(exponent_value);
    }
    else
    {
        cout << "Interval out of bound" << endl;
        fx_value = 1.0;
    }

    return fx_value;
}