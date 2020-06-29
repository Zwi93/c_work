/************************************************************************************************************************************
 * Purpose: Given the correlation matrix onecan price the fair spread of a basket CDS using functions defined here.                 * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Usage: Provide the correlation matrix and the script will compute the fair basket spread.                                        *
 *                                                                                                                                  *
 ************************************************************************************************************************************
 */

//Include all relevant header files here.
#include <iostream>
#include <cmath>
using namespace std;

//Declare important macros here.
#define No_COMPANIES 3 //number of underlyings in the basket.
#define NATURAL_EXP exp(1)
#define MY_PI 4*atan(1.0)  //pi to be used only in this script.

//Functions Declaration here.
void get_pseudo_square_root (double correlation_matrix[][No_COMPANIES], double pseudo_matrix[][No_COMPANIES]);
double inverse_error_function (int order, double x_param);
double inverse_normal_cdf (double x_param);
double factorial_of_x (int x_param);
double beta_function (double a_param, double b_param);
long double incomplete_beta_function (double a_param, double b_param, double x_variable);
long double hypergeometric_function (int order, double a_param, double b_param, double c_param, double x_variable);
void system_call ();

int main ()
{
    //Initialize the correlation matrix.
    double correlation_marix[No_COMPANIES][No_COMPANIES];
    correlation_marix[0][0] = 4.0;
    correlation_marix[0][1] = 12.0;
    correlation_marix[0][2] = -16.0;
    correlation_marix[1][0] = 12.0;
    correlation_marix[1][1] = 37.0;
    correlation_marix[1][2] = -43.0;
    correlation_marix[2][0] = -16.0;
    correlation_marix[2][1] = -43.0;
    correlation_marix[2][2] = 98.0;

    //Initialize the pseudo-square root matrix with 0s.
    double pseudo_matrix[No_COMPANIES][No_COMPANIES];
    int outer_index, inner_index;

    for (outer_index = 0; outer_index < No_COMPANIES; outer_index++)
    {
        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            pseudo_matrix[outer_index][inner_index] = 0.0;
        }
    }

    /*
    //Perform the Cholesky decomposition.
    get_pseudo_square_root(correlation_marix, pseudo_matrix);

    for (outer_index = 0; outer_index < No_COMPANIES; outer_index++)
    {
        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            cout << pseudo_matrix[outer_index][inner_index] << endl;
        }
    }
    
    double test;
    test = inverse_error_function(100, erf(1.3));

    cout << "Inverse error function " << test << endl;

    double reg_beta_1, reg_beta_2;
    reg_beta_1 = incomplete_beta_function(0.6, 0.5, 0.8999)/beta_function(0.6, 0.5);
    reg_beta_2 = 1 - incomplete_beta_function(0.5, 0.6, 1 - 0.8999)/beta_function(0.5, 0.6);
    //cout << "LHS " << reg_beta_1 << endl;
    //cout << "RHS " << reg_beta_2 << endl;*/
    system_call();

    return 0;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the Cholesky decomposition for given correlation matrix.                                            * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * correlation_matrix: matrix storing information about the correlations of the variables.                                          *
 * pseudo_matrix: matrix to store the computed pseudo-square root matrix.                                                           *
 *                                                                                                                                  *
 * Return: This is a void function.                                                                                                 *                                                                                                                                  
 ************************************************************************************************************************************
 */
void get_pseudo_square_root (double correlation_matrix[][No_COMPANIES], double pseudo_matrix[][No_COMPANIES])
{
    int outer_index, inner_index;

    for (outer_index = 0; outer_index < No_COMPANIES; outer_index++)
    {
        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            if (inner_index == outer_index)
            {
                double temporary_sum = 0.0;
                int sum_index;

                for (sum_index = 0; sum_index < inner_index; sum_index++)
                {
                    temporary_sum += pow(pseudo_matrix[inner_index][sum_index], 2);
                }
                pseudo_matrix[outer_index][inner_index] = sqrt(correlation_matrix[inner_index][inner_index] - temporary_sum); 
            }

            else if (inner_index < outer_index)
            {
                double temporary_sum = 0.0;
                int sum_index;
                
                for (sum_index = 0; sum_index < inner_index; sum_index++)
                {
                    temporary_sum += pseudo_matrix[outer_index][sum_index]*pseudo_matrix[inner_index][sum_index];
                }
                pseudo_matrix[outer_index][inner_index] = (correlation_matrix[outer_index][inner_index] - temporary_sum)/pseudo_matrix[inner_index][inner_index];
            }

            else
            { 
                pseudo_matrix[outer_index][inner_index] = 0.0;
            }
            
        }
    }
}

/************************************************************************************************************************************
 * Purpose: Function to compute the cummulative density function for normal RVs.                                                    * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * x_param: The x-value in the range (0, infinity).                                                                                 *
 *                                                                                                                                  *
 * Return: The corresponding probability of the rv to be lower than x_param.                                                        *                                                                                                                                  
 ************************************************************************************************************************************
 */
double normal_cdf (double x_param)
{
    double normal_cdf;
    double new_param = x_param/sqrt(2);

    normal_cdf = 0.5 + 0.5*erf(new_param);

    return normal_cdf;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the inverse normal cdf. It can be used to convert uniform RVs to normal RVs.                        * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * order: The degree of the highest polynomial in the series approximation function to the error function.                          *
 * x_param: the input value.                                                                                                        *
 *                                                                                                                                  *
 * Return: The return value is the quartile value corresponding to x_parameter.                                                     *                                                                                                                                  
 ************************************************************************************************************************************
 */

double inverse_normal_cdf (int order, double x_param)
{
    double inverse_normal_cdf;

    inverse_normal_cdf = sqrt(2)*inverse_error_function(order, 2*x_param - 1);

    return inverse_normal_cdf;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the inverse function to the error function from it's series approximation.                          * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * order: The degree of the highest polynomial in the series approximation function to the error function.                          *
 * x_param: the input value.                                                                                                        *
 *                                                                                                                                  *
 * Return: The return value is the quartile value corresponding to x_parameter.                                                     *                                                                                                                                  
 ************************************************************************************************************************************
 */
double inverse_error_function (int order, double x_param)
{
    //Array to hold the coefficients.
    double coefficients_array[order];

    //Initialize 1st known coefficient.
    coefficients_array[0] = 1;

    //The 1st value to the series approximation.
    double inverse_error_value = sqrt(MY_PI)*x_param/2;
    

    int outer_index, inner_index;

    //Approximate the inverse error function using it's series approximation formula.
    for (outer_index = 1; outer_index < order; outer_index++)
    {
        double coefficient = 1.0;
        
        for (inner_index = 0; inner_index < outer_index - 1; inner_index++)
        {
            coefficient += (coefficients_array[inner_index]*coefficients_array[outer_index - inner_index - 1])/((inner_index + 1)*(2*inner_index + 1));
        }

        coefficients_array[outer_index] = coefficient;
        inverse_error_value += (pow(-1, outer_index)*coefficients_array[outer_index]*pow(sqrt(MY_PI)*x_param/2, 2*outer_index + 1))/(2*outer_index + 1);
    }

    return inverse_error_value;
}

long double hypergeometric_function (int order, double a_param, double b_param, double c_param, double x_variable)
{
    int index;
    long double hypergeometric_value;
    long double temporary_sum = (tgamma(a_param)*tgamma(b_param))/tgamma(c_param);
    
    for (index = 1; index < order; index++)
    {
        temporary_sum += (tgamma(a_param + index)*tgamma(b_param + index)*pow(x_variable, index))/(tgamma(c_param + index)*factorial_of_x(index));
        if (index > (order - 5))
        {
            //cout << tgamma(a_param + index) << endl;
            //cout << tgamma(b_param + index) << endl;
            //cout << tgamma(c_param + index) << endl;
            //cout << pow(x_variable, index) << endl;
            //cout << factorial_of_x(index) << endl;
            //cout << "temp sum " << temporary_sum << endl;
        } 
        
    }

    hypergeometric_value = (tgamma(c_param)*temporary_sum)/(tgamma(a_param)*tgamma(b_param));

    return hypergeometric_value;
}

long double incomplete_beta_function (double a_param, double b_param, double x_variable)
{
    long double beta_value;

    beta_value = pow(x_variable, a_param)*hypergeometric_function(95, a_param, 1 - b_param, a_param + 1, x_variable)/a_param;

    return beta_value;
}

double beta_function (double a_param, double b_param)
{
    double beta_value;
    beta_value = tgamma(a_param)*tgamma(b_param)/tgamma(a_param + b_param);

    return beta_value;
}

double factorial_of_x (int x_param)
{
    int index;
    double factorial = 1.0;

    if (x_param < 31)
    {
        for (index = 1; index <= x_param; index++)
        {
            factorial = factorial*index;
        }
    }
    else
    {
        factorial = sqrt(2*MY_PI*x_param)*pow(x_param/NATURAL_EXP, x_param);
    }

    return factorial;
}

void system_call ()
{
    string command = "python3 correlation_calcs.py";
    const char *c_commdand = command.c_str();
    system(c_commdand);

}