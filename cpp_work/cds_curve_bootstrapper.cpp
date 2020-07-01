/************************************************************************************************************************************
 * Purpose: Basic CDS curve bootstrapper. Script takes the CDS curve and calculates the risk-neutral survival probabilities.        * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Usage: Run the program and it will print out the bootstrapped survival probabilities.                                            *
 *                                                                                                                                  *
 ************************************************************************************************************************************
 */

#include "cds_curves.h"

int main ()
{
    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    contract_info cds_info[6];
    cds_info[0] = {"0.5Y cds", 100, 0.0, 0.5};
    cds_info[1] = {"1Y cds", 100, 0.0, 1.0};
    cds_info[2] = {"2Y cds", 114.00, 0.0, 2.0};
    cds_info[3] = {"3Y cds", 121.0, 0.0, 3};
    cds_info[4] = {"4Y cds", 135.0, 0.0, 4};
    cds_info[5] = {"5Y cds", 145.0, 0.0, 5.0};

    //Obtain the bootstrapped zero yields from bonds' prices.
    double risk_free_df[11];  //Array to store the bootstrapped zero discount factors.
    //bond_curve_bootstrapper(risk_free_df); //function to bootstrapp bond curve.

    //Initiate input variables.
    double survival_probability[11];
    double hazard_rates[11];
    double LGD = 0.4;

    //Bootstrapp cds curve.
    cds_curve_bootstrapper(survival_probability, cds_info, LGD);

    //Get hazard rates.
    get_hazard_rates(survival_probability, hazard_rates);
    double index = survival_time_inverse_cdf(hazard_rates, 0.5);

    cout << "Index with minimum difference " << index << endl;
    
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
void cds_curve_bootstrapper (double survival_probability[11], contract_info cds_info[6],double LGD = 0.4)
{

    //interpolate the cds curve.
    contract_info interpolated_cds_info[10];
    interpolate_par_curve1(cds_info, interpolated_cds_info);

    //Obtain the bootstrapped zero yields from bonds' prices.
    double risk_free_df[11];  //Array to store the bootstrapped zero discount factors.
    bond_curve_bootstrapper(risk_free_df); //function to bootstrapp bond curve.

    cout << endl;

    //Initialize useful variable.
    int index;

    //Initialize array with 1s.
    for (index = 0; index < 11; index++)
    {
        survival_probability[index] = 1.0;
    }

    //Begin bootstrapping here.
    //First calculate the 1st implied survival probability.
    survival_probability[1] = LGD/(LGD + interpolated_cds_info[0].price/pow(10, 4));

    //Then calculate the 2nd, 3rd etc...
    for (index = 2; index < 11; index++)
    {
        double temp_calc = 0;  //Variable to store summation. Only needed in this scope.
        int inner_index;

        for (inner_index = 1; inner_index < index; inner_index++)
        {
            temp_calc += risk_free_df[inner_index]*(LGD*survival_probability[inner_index - 1] - (LGD + 0.5*interpolated_cds_info[index - 1].price/pow(10, 4))*survival_probability[inner_index]);
        }

        //spreads are divived by 10^4 for conversion to %. And also by 2 to convert to semi-annual.
        survival_probability[index] = temp_calc/(risk_free_df[index]*(LGD + 0.5*interpolated_cds_info[index - 1].price/pow(10, 4))) + survival_probability[index - 1]*LGD/(LGD + 0.5*interpolated_cds_info[index - 1].price/pow(10, 4)); 
    }

    //Print out the results.
    for (index = 1; index < 11; index++)
    {
        cout << interpolated_cds_info[index - 1].name + " survival probability\n" << survival_probability[index] << endl;
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
    // Create array to carry the information of bonds to be bootstrapped. Data taken on 2020/06/26 for US Treasury.
    contract_info bonds_info[6];
    bonds_info[0] = {"0.5Y bond", 0.00167, 0.0, 0.5};
    bonds_info[1] = {"1Y bond", 0.00162, 0.0, 1.0};
    bonds_info[2] = {"2Y bond", 0.00168, 0.0013, 2.0};
    bonds_info[3] = {"3Y bond", 0.00186, 0.0013, 3};
    bonds_info[4] = {"4Y bond", 0.00236, 0.0015, 4};  //Interpolated.
    bonds_info[5] = {"5Y bond", 0.003, 0.0025, 5.0};

    //contract_info *interpolated_bonds_info;
    //interpolated_bonds_info = interpolate_par_curve(bonds_info, 2);
    contract_info interpolated_bonds_info[10];
    interpolate_par_curve1(bonds_info, interpolated_bonds_info);

    //Initialize element 0 for zero_disc_factor array with 0. This is needed to bootstrapp properly, loop following depends on this.
    zero_disc_factor[0] = 0.0;

    //Begin the bootstrapp here.
    int index;

    for (index = 1; index < 11; index++)
    {
        double current_bond_price = bond_price_from_yield(interpolated_bonds_info[index - 1].price, interpolated_bonds_info[index - 1].coupon, 1.0, interpolated_bonds_info[index - 1].maturity);
        double temp_factor = 0;

        cout << interpolated_bonds_info[index - 1].name + " price\n";
        cout << current_bond_price << endl; 

        int inner_index;
        for (inner_index = 0; inner_index < index; inner_index++)
        {
            temp_factor += zero_disc_factor[inner_index]*interpolated_bonds_info[inner_index].coupon/FREQUENCY;
        }

        zero_disc_factor[index] = (current_bond_price - temp_factor)/(interpolated_bonds_info[index - 1].coupon/FREQUENCY + 1);  //Face value is one for now.
    }
    cout << endl;

    for (index = 1; index < 11; index++)
    {
        cout << interpolated_bonds_info[index - 1].name + " zero factor\n" << zero_disc_factor[index] << endl;
    }
}

/************************************************************************************************************************************
 * Purpose: Function definition for the exponential interpolation technique.                                                        * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * x_input is the date at which to interpolate, a_param, b_params are known and fa_param fb_param are their corresponding .         *
 * evalueated values.                                                                                                               *
 * Return: fx_value, the interpolated value at x date.                                                                              *
 ************************************************************************************************************************************
 */
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

/************************************************************************************************************************************
 * Purpose: Function to perform the interpolation of bonds/cds curves from available term structure.                                * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * x_input is the date at which to interpolate, a_param, b_params are known and fa_param fb_param are their corresponding .         *
 * evalueated values.                                                                                                               *
 * Return: This is a void function.                                                                                                 *
 ************************************************************************************************************************************
 */
struct contract_info *interpolate_par_curve (contract_info info_struct[6], int frequency)
{
    //Initialize useful variable.
    int index, running_index = 0;

    //Interpolate yields.
    contract_info interpolated_info[frequency*(6 - 1)];

    interpolated_info[0] = info_struct[0];

    for (index = 1; index < (6 - 1); index++)
    {
        double a_param, b_param, fa_param, fb_param;  //These go into the exponential interpolator.
        running_index += 1; //This tracks the index of interpolated_info array, which runs faster.

        //At points of known value, no need to interpolate.
        interpolated_info[running_index] = info_struct[index];

        a_param = info_struct[index].maturity;
        b_param = info_struct[index + 1].maturity;
        fa_param = info_struct[index].price;
        fb_param = info_struct[index + 1].price;

        //Interpolate between the nearest points.
        running_index += 1;
        interpolated_info[running_index].name = to_string(a_param + 0.5) + "Y bond";
        interpolated_info[running_index].coupon = info_struct[index + 1].coupon;
        interpolated_info[running_index].maturity = a_param + 0.5; 
        interpolated_info[running_index].price = exponential_interpolation(a_param + 0.5, a_param, b_param, fa_param, fb_param);
    }

    interpolated_info[FREQUENCY*(6 - 1) - 1] = interpolated_info[6 - 1];

    return interpolated_info;
}

/************************************************************************************************************************************
 * Purpose: Function to perform the interpolation of bonds/cds curves from available term structure. Uses different data types.     * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * x_input is the date at which to interpolate, a_param, b_params are known and fa_param fb_param are their corresponding .         *
 * evalueated values.                                                                                                               *
 * Return: This is a void function.                                                                                                 *
 ************************************************************************************************************************************
 */
void interpolate_par_curve1 (contract_info info_struct[6], contract_info interpolated_info[2*(6 - 1)])
{
    //Initialize useful variable.
    int index, running_index = 0;

    //Interpolate yields.
    interpolated_info[0] = info_struct[0];

    for (index = 1; index < (6 - 1); index++)
    {
        double a_param, b_param, fa_param, fb_param;  //These go into the exponential interpolator.
        running_index += 1; //This tracks the index of interpolated_info array, which runs faster.

        //At points of known value, no need to interpolate.
        interpolated_info[running_index] = info_struct[index];

        a_param = info_struct[index].maturity;
        b_param = info_struct[index + 1].maturity;
        fa_param = info_struct[index].price;
        fb_param = info_struct[index + 1].price;

        //Interpolate between the nearest points.
        running_index += 1;
        interpolated_info[running_index].name = to_string(a_param + 0.5) + "Y bond";
        interpolated_info[running_index].coupon = info_struct[index + 1].coupon;
        interpolated_info[running_index].maturity = a_param + 0.5; 
        interpolated_info[running_index].price = exponential_interpolation(a_param + 0.5, a_param, b_param, fa_param, fb_param);
    }

    interpolated_info[FREQUENCY*(6 - 1) - 1] = info_struct[6 - 1];

}

double bond_price_from_yield (double yield, double coupon_rate, double par_value, double bond_maturity)
{
/*
Function to compute the price of a bond given its yield, coupon rate, and maturity. Zero coupons bonds are special cases of these.
*/
    int index, max_coupon_payment = (int) FREQUENCY*bond_maturity;
    double bond_value = 0.0;
    double coupon_date = 0.0;

    for (index = 1; index <= max_coupon_payment; index++)
    {
        coupon_date = index/FREQUENCY; 
        bond_value += 0.5*coupon_rate*exp(-yield*coupon_date);
    }

    bond_value += par_value*exp(-yield*bond_maturity);
    
    return bond_value; 
}

/************************************************************************************************************************************
 * Purpose: Function to obtain the hazard rates from the survival probabilities using a piece-wise constant function.               * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * survival_probability array carries the probabilities of survival, and hazard rates array will carry the output rates             *
 *                                                                                                                                  *
 * Return: This is a void function.                                                                                                 *
 ************************************************************************************************************************************
 */
void get_hazard_rates (double survival_probability[11], double hazard_rates[11])
{
    //Assume contant time interval between survival probabilities.
    double time_interval = 0.5, minus_one = -1;
    int outer_index, inner_index;

    for (outer_index = 1; outer_index < 11; outer_index++)
    {
        double temporary_sum = 0.0;

        for (inner_index = 1; inner_index < outer_index; inner_index++)
        {
            temporary_sum += log(survival_probability[inner_index]);
        }

        hazard_rates[outer_index] = minus_one*(log(survival_probability[outer_index]) + temporary_sum)/time_interval;
    }

    for (outer_index = 1; outer_index < 11; outer_index++)
    {
        cout << "hazard rates " << hazard_rates[outer_index] << endl;
    }
}

/************************************************************************************************************************************
 * Purpose: Function to obtain the inverse cdf for default time given piece-wise constant hazard rates.                             * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * hazard_rates array carries the mentioned rates, and x_input is the function independent variable.                                *
 *                                                                                                                                  *
 * Return: This returns the corresponding y_value of the function.                                                                  *
 ************************************************************************************************************************************
 */
double survival_time_inverse_cdf (double hazard_rates[11], double x_input)
{
    //Method employed is not robust but uses only the built exp function.
    int index = 0;
    double time_interval = 0.5, exponent_sum = 0;
    double difference_variable1 = 1, difference_variable2 = 1; //Needed to determine the difference and minimize it.

    while (difference_variable1*difference_variable2 > 0 & index < 11)
    {
        index += 1;
        exponent_sum += hazard_rates[index]*time_interval;
        
        difference_variable1 = x_input - exp(-exponent_sum);

        difference_variable2 = x_input - exp(-exponent_sum -hazard_rates[index + 1]*time_interval);

        cout << "Difference variable 1 " << difference_variable1 << endl;
        cout << "Difference variable 2 " << difference_variable2 << endl; 

    }

    return index;
}