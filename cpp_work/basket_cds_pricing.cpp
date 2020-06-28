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
#define MY_PI 4*atan(1.0)  //pi to be used only in this script.

//Functions Declaration here.
void get_pseudo_square_root (double correlation_matrix[][No_COMPANIES], double pseudo_matrix[][No_COMPANIES]);
double inverse_error_function (int order, double x_param);
double inverse_normal_cdf (double x_param);

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
    test = inverse_error_function(1000, erf(0.3));

    cout << test << endl;
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

double inverse_normal_cdf (double x_param)
{
    double inverse_normal_cdf;

    inverse_normal_cdf = sqrt(2)*inverse_error_function(10, x_param - 1);

    return inverse_normal_cdf;
}

double inverse_error_function (int order, double x_param)
{
    double coefficients_array[order];  //Array to hold the coefficients.
    //Initialize 1st known coefficient.
    coefficients_array[0] = 1;

    double inverse_error_value = sqrt(MY_PI)*x_param/2;
    

    int outer_index, inner_index;

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