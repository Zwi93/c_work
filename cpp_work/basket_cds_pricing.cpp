/************************************************************************************************************************************
 * Purpose: Given the correlation matrix one can price the fair spread of a basket CDS using functions defined here.                * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Usage: Provide the correlation matrix and the script will compute the fair basket spread.                                        *
 *                                                                                                                                  *
 ************************************************************************************************************************************
 */

//Include all relevant header files here.
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include "cds_curve_bootstrapper.h"

using namespace std;

//Declare important macros here.
#define No_COMPANIES 5 //number of underlyings in the basket.
#define SIMULATIONS 3
#define NATURAL_EXP exp(1)
#define MY_PI 4*atan(1.0)  //pi to be used only in this script.
#define size_one 3

//Functions Declaration here.
void get_pseudo_square_root (double correlation_matrix[][No_COMPANIES], double pseudo_matrix[][No_COMPANIES]);
double normal_cdf (double x_param);
double inverse_error_function (int order, double x_param);
double inverse_normal_cdf (int order, double x_param);
double factorial_of_x (int x_param);
double beta_function (double a_param, double b_param);
long double incomplete_beta_function (double a_param, double b_param, double x_variable);
long double hypergeometric_function (int order, double a_param, double b_param, double c_param, double x_variable);
void get_correlation_matrix (double correlation_array[][No_COMPANIES]);
void one_to_many_dimension (double one_dimension_array[No_COMPANIES], double many_dimension_array[][No_COMPANIES]);
void matrix_product (double array_one[][No_COMPANIES], double array_two[][No_COMPANIES], double product_array[][No_COMPANIES], double scale_factor);
double inverse_error_function1 (double x_param);
void basket_cds_mc_pricing (int no_of_credits, int no_of_simulations, int order, contract_info cds_curves_matrix[No_COMPANIES][6], double LGD);
double get_minimum_value (double array[No_COMPANIES]);
double get_nth_minimum_value (double array[No_COMPANIES], int n);

int main ()
{
    //Initialize the correlation matrix.
    //double correlation_array[5][5];
    //get_correlation_matrix(correlation_array);

    //Creeate a 5 by 6 array to hold all these credit curves.
    contract_info cds_curves_matrix[No_COMPANIES][6];

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[0][0] = {"0.5Y cds", 95, 0.0, 0.5};
    cds_curves_matrix[0][1] = {"1Y cds", 100, 0.0, 1.0};
    cds_curves_matrix[0][2] = {"2Y cds", 114.00, 0.0, 2.0};
    cds_curves_matrix[0][3] = {"3Y cds", 121.0, 0.0, 3};
    cds_curves_matrix[0][4] = {"4Y cds", 135.0, 0.0, 4};
    cds_curves_matrix[0][5] = {"5Y cds", 145.0, 0.0, 5.0};

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[1][0] = {"0.5Y cds", 85, 0.0, 0.5};
    cds_curves_matrix[1][1] = {"1Y cds", 105, 0.0, 1.0};
    cds_curves_matrix[1][2] = {"2Y cds", 110.00, 0.0, 2.0};
    cds_curves_matrix[1][3] = {"3Y cds", 126.0, 0.0, 3};
    cds_curves_matrix[1][4] = {"4Y cds", 135.0, 0.0, 4};
    cds_curves_matrix[1][5] = {"5Y cds", 140.0, 0.0, 5.0};

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[2][0] = {"0.5Y cds", 75, 0.0, 0.5};
    cds_curves_matrix[2][1] = {"1Y cds", 89, 0.0, 1.0};
    cds_curves_matrix[2][2] = {"2Y cds", 104.00, 0.0, 2.0};
    cds_curves_matrix[2][3] = {"3Y cds", 117.0, 0.0, 3};
    cds_curves_matrix[2][4] = {"4Y cds", 130.0, 0.0, 4};
    cds_curves_matrix[2][5] = {"5Y cds", 141.0, 0.0, 5.0};

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[3][0] = {"0.5Y cds", 85, 0.0, 0.5};
    cds_curves_matrix[3][1] = {"1Y cds", 101, 0.0, 1.0};
    cds_curves_matrix[3][2] = {"2Y cds", 104.00, 0.0, 2.0};
    cds_curves_matrix[3][3] = {"3Y cds", 111.0, 0.0, 3};
    cds_curves_matrix[3][4] = {"4Y cds", 125.0, 0.0, 4};
    cds_curves_matrix[3][5] = {"5Y cds", 125.0, 0.0, 5.0};

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[4][0] = {"0.5Y cds", 45, 0.0, 0.5};
    cds_curves_matrix[4][1] = {"1Y cds", 50, 0.0, 1.0};
    cds_curves_matrix[4][2] = {"2Y cds", 61.00, 0.0, 2.0};
    cds_curves_matrix[4][3] = {"3Y cds", 71.0, 0.0, 3};
    cds_curves_matrix[4][4] = {"4Y cds", 75.0, 0.0, 4};
    cds_curves_matrix[4][5] = {"5Y cds", 85.0, 0.0, 5.0};

    /*
    //Toy model for correlation matrix.
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
    
    double n_1d_array[No_COMPANIES] = {1, 1, 1};
    double n_by_n_array[No_COMPANIES][No_COMPANIES];
    double product_array[No_COMPANIES][No_COMPANIES];
    one_to_many_dimension(n_1d_array, n_by_n_array);
    matrix_product(correlation_marix, n_by_n_array, product_array, 1.0);


    //Initialize the pseudo-square root matrix with 0s.
    double pseudo_matrix[No_COMPANIES][No_COMPANIES];
    int outer_index, inner_index;

    for (outer_index = 0; outer_index < No_COMPANIES; outer_index++)
    {
        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            cout << product_array[outer_index][inner_index] << endl;
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
    
    double test, x_input = erf(-2.3);
    test = inverse_error_function1(x_input);
    //test = inverse_error_function(100, 0.5);

    cout << "Inverse error function " << test << endl;
    /*
    double reg_beta_1, reg_beta_2;
    reg_beta_1 = incomplete_beta_function(0.6, 0.5, 0.8999)/beta_function(0.6, 0.5);
    reg_beta_2 = 1 - incomplete_beta_function(0.5, 0.6, 1 - 0.8999)/beta_function(0.5, 0.6);
    //cout << "LHS " << reg_beta_1 << endl;
    //cout << "RHS " << reg_beta_2 << endl;*/

    double LGD = 0.4; //Loss Given Default, assumed constant and equal for each company.

    //basket_cds_mc_pricing(No_COMPANIES, SIMULATIONS, 0, cds_curves_matrix, LGD);
    double array[No_COMPANIES] = {2.5, 1.4, 4.5, 1.2, 0.6};
    double minimum_value = get_minimum_value(array);

    cout << "Min " << minimum_value << endl;


    return 0;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the spread for the basket cds using monte carlo techniques.                                         * 
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
void basket_cds_mc_pricing (int no_of_credits, int no_of_simulations, int order, contract_info cds_curves_matrix[No_COMPANIES][6], double LGD)
{
    int index;

    for (index = 0; index < no_of_simulations; index++)
    {
        int inner_index; double uniform_rvs[no_of_credits];  //Array to store univariates.

        for (inner_index = 0; inner_index < no_of_credits; inner_index++)
        {
            uniform_rvs[inner_index] = ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
        }

        double normal_rvs[No_COMPANIES], normal_rvs_matrix[No_COMPANIES][No_COMPANIES]; // Array to store corresponding normals.

        for (inner_index = 0; inner_index < no_of_credits; inner_index++)
        {
            normal_rvs[inner_index] = inverse_normal_cdf(order, uniform_rvs[inner_index]);
        }
        
        //Convert the 1d normals array to 2d.
        one_to_many_dimension(normal_rvs, normal_rvs_matrix);

        double correlated_normals[No_COMPANIES][No_COMPANIES], correlation_matrix[No_COMPANIES][No_COMPANIES], pseudo_matrix[No_COMPANIES][No_COMPANIES];

        //Get the correlation matrix and store in variable correlation_matrix and compute the cholesky decomposition.
        get_correlation_matrix(correlation_matrix);
        get_pseudo_square_root(correlation_matrix, pseudo_matrix);

        //Get the correlated normal RVs;the values are stored in the 1st column.
        matrix_product(pseudo_matrix, normal_rvs_matrix, correlated_normals, 1.0);

        double correlated_default_times[No_COMPANIES]; //Variable to store the correlated default time for each credit.
        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            double correlated_uniform_rv;
            correlated_uniform_rv = normal_cdf(correlated_normals[inner_index][0]);

            cout << "Correlated univariates " << correlated_uniform_rv << endl;

            //Construct the credit curves fo each counterpart.
            contract_info cds_info[6];

            int tenor_index; //The tenor of the curve point.
            for (tenor_index = 0; tenor_index < 6; tenor_index++)
            {
                cds_info[tenor_index] = cds_curves_matrix[inner_index][tenor_index];
            }

            //Obtain the survival probabilities for counterpart corresponding to index inner_index.
            double survival_probability[11];

            cds_curve_bootstrapper(survival_probability, cds_info, LGD);

            //Next from the survival probabilities, get the hazard rates.
            double hazard_rates[11];
            get_hazard_rates(survival_probability, hazard_rates);
            
            //Then obtain the correlated default time.
            correlated_default_times[inner_index] = survival_time_inverse_cdf(hazard_rates,1 - correlated_uniform_rv, 1000, 0.001);

            cout << "Correlated default time for Counterpart " << inner_index << " " << correlated_default_times[inner_index] << endl;
        }

    }
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

    if (order == 0)
        inverse_normal_cdf = sqrt(2)*inverse_error_function1(2*x_param - 1);
    if (order == 0)
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

/************************************************************************************************************************************
 * Purpose: Function to compute the inverse function to the error function from one of it's explicit approximation.                 * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * x_param: the input value.                                                                                                        *
 *                                                                                                                                  *
 * Return: The return value is the quartile value corresponding to x_parameter.                                                     *                                                                                                                                  
 ************************************************************************************************************************************
 */
double inverse_error_function1 (double x_param)
{
    double log_term, a_param, inner_sqrt_term; //Parameters to simplify explicit function.
    double inverse_error_value;

    log_term = log(1 - x_param*x_param);
    a_param = (8*MY_PI - 24)/(12*MY_PI - 3*MY_PI*MY_PI);
    inner_sqrt_term = sqrt(pow(2/(MY_PI*a_param) + log_term/2, 2) - (1/a_param)*log_term);

    inverse_error_value = sqrt(-2/(MY_PI*a_param) - log_term/2 + inner_sqrt_term);

    if (x_param < 0) 
        return -inverse_error_value;
    if (x_param > 0)
        return inverse_error_value;
    if (x_param == 0)
        return 0.0;
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
    //Function to compute the factorial of x_param, with sterling formula used for large x_param. 
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
/************************************************************************************************************************************
 * Purpose: Function to get the correlation matrix;calculations are done from a python script and saved into a file which is read-in*                          
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * correlation array to store the matrix computed in the python script.                                                             *
 *                                                                                                                                  *
 * This is a void function.                                                                                                         *                                                                                                                                  
 ************************************************************************************************************************************
 */
void get_correlation_matrix (double correlation_array[][No_COMPANIES])
{
    string command = "python3 correlation_calcs.py";  //Command to run on the shell.
    const char *c_command = command.c_str();
    system(c_command);

    char correlation_file[50] = "correlation_matrix.txt";
    ifstream stream_to_file(correlation_file);
    int index1, index2, outer_index = 0; string line;

    //Read from the text file saved from the python script execution.
    while (getline(stream_to_file, line)) 
    {
        string word;
        istringstream string_stream (line);
        int inner_index = 0;
        while (getline(string_stream, word, ' '))
        {
            correlation_array[outer_index][inner_index] = stod(word);
            inner_index++;
        }
        outer_index++;
            
    }

    stream_to_file.close();
    
    /*for (index1 = 0; index1 < 5; index1++)
    {
        for (index2 = 0; index2 < 5; index2++)
        {
            cout <<index1 << index2 << " " << correlation_array[index1][index2] << endl;
        }    
    }*/   
}

void matrix_product (double array_one[][No_COMPANIES], double array_two[][No_COMPANIES], double product_array[][No_COMPANIES], double scale_factor)
{
    int i_index, j_index;

    for (i_index = 0; i_index < No_COMPANIES; i_index++)
    {
        for (j_index = 0; j_index < No_COMPANIES; j_index++)
        {
            int k_index;
            double temporary_sum = 0;
            for (k_index = 0; k_index < No_COMPANIES; k_index++)
            {
                temporary_sum += array_one[i_index][k_index]*array_two[k_index][j_index];
            }

            product_array[i_index][j_index] = scale_factor*temporary_sum;
        }
    }
}

void one_to_many_dimension (double one_dimension_array[No_COMPANIES], double many_dimension_array[][No_COMPANIES])
{
    int outer_index, inner_index;

    for (outer_index = 0; outer_index < size_one; outer_index++)
    {
        for (inner_index = 0; inner_index < size_one; inner_index++)
        {
            if (inner_index == 0)
            {
                many_dimension_array[outer_index][inner_index] = one_dimension_array[inner_index];
            }
            else
            {
                many_dimension_array[outer_index][inner_index] = 0.0;
            }
            
        }
    }
}





void cds_curve_bootstrapper (double survival_probability[11], contract_info cds_info[6], double LGD)
{

    //interpolate the cds curve.
    contract_info interpolated_cds_info[10];
    interpolate_par_curve1(cds_info, interpolated_cds_info);

    //Obtain the bootstrapped zero yields from bonds' prices.
    double risk_free_df[11];  //Array to store the bootstrapped zero discount factors.
    bond_curve_bootstrapper(risk_free_df); //function to bootstrapp bond curve.

    //cout << endl;

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

    /*
    //Print out the results.
    for (index = 1; index < 11; index++)
    {
        cout << interpolated_cds_info[index - 1].name + " survival probability\n" << survival_probability[index] << endl;
    }*/
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

        //cout << interpolated_bonds_info[index - 1].name + " price\n";
        //cout << current_bond_price << endl; 

        int inner_index;
        for (inner_index = 0; inner_index < index; inner_index++)
        {
            temp_factor += zero_disc_factor[inner_index]*interpolated_bonds_info[inner_index].coupon/FREQUENCY;
        }

        zero_disc_factor[index] = (current_bond_price - temp_factor)/(interpolated_bonds_info[index - 1].coupon/FREQUENCY + 1);  //Face value is one for now.
    }
    cout << endl;

    /*
    for (index = 1; index < 11; index++)
    {
        cout << interpolated_bonds_info[index - 1].name + " zero factor\n" << zero_disc_factor[index] << endl;
    }*/
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
*/


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
        hazard_rates[outer_index] = (log(survival_probability[outer_index - 1]) - log(survival_probability[outer_index]))/time_interval;
    }

    /*
    for (outer_index = 1; outer_index < 11; outer_index++)
    {
        cout << "hazard rates " << hazard_rates[outer_index] << endl;
    }*/
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
double survival_time_inverse_cdf (double hazard_rates[11], double x_input, int divisions, double accuracy_level)
{
    //Method employed is not robust but uses only the built in exp function.
    int index = 0;
    double time_interval = 0.5, exponent_sum = 0;
    double difference_variable1 = 1, difference_variable2 = 1; //Needed to determine the difference and minimize it.

    while (difference_variable1*difference_variable2 > 0 & index < 11)
    {
        index += 1;
        exponent_sum += hazard_rates[index]*time_interval;
        
        difference_variable1 = x_input - exp(-exponent_sum);

        difference_variable2 = x_input - exp(-exponent_sum -hazard_rates[index + 1]*time_interval);

    }

    //cout << "Index stopped at " << index << endl;
    //Interval of intercept.
    double lower_bound = index*time_interval, upper_bound = lower_bound + time_interval;

    //cout << "Lower bound is " << lower_bound << endl;

    //Pick many values in this interval and evaluate difference to input value.
    double estimated_value = lower_bound, difference_variable3 = 1, delta_time = time_interval/divisions;

    while (abs(difference_variable3) > accuracy_level & estimated_value < upper_bound)
    {
        estimated_value += delta_time;
        difference_variable3 = x_input - exp(-exponent_sum - hazard_rates[index + 1]*(estimated_value - lower_bound));
    }
     

    return estimated_value;
}

double survival_time_inverse_cdf1 (double hazard_rates[11], double x_input, double time_interval)
{
    double h_bar = -log(x_input)/time_interval;
    double running_sum = h_bar;

    cout << "h-bar " << h_bar << endl; 
    
    int index = 0;

    while(running_sum > 0 & index < 11)
    {
        index += 1;
        running_sum = running_sum - hazard_rates[index];

        cout << "Running difference " << running_sum << endl; 
    }

    double y_value = (running_sum + hazard_rates[index])*time_interval/hazard_rates[index + 1] + time_interval*index; 
    
    return y_value;
}

double get_minimum_value (double array[No_COMPANIES])
{
    int outer_index, inner_index, minimum_index;
    double minimum_value;

    for (outer_index = 0; outer_index < No_COMPANIES; outer_index++)
    {    
        double qoutient_array[No_COMPANIES - 1];
        int i = -1, selection_index[No_COMPANIES - 1];

        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            if (inner_index != outer_index)
            {
                ++i; selection_index[i] = inner_index;
            }
        }

        int greater_than_1 = 0;
        for (inner_index = 0; inner_index < (No_COMPANIES - 1); inner_index++)
        {
            double denom, numerator; 
            numerator = array[selection_index[inner_index]];
            denom = array[outer_index];
            qoutient_array[inner_index] = numerator/denom;

            if (qoutient_array[inner_index] > 1)
                greater_than_1++;
            if (qoutient_array[inner_index] < 1)
                continue;
            
        }

        if (greater_than_1 == (No_COMPANIES - 1))
            minimum_index  = outer_index;
        else 
            continue;
    }

    minimum_value = array[minimum_index];
    return minimum_value;
}

double get_nth_minimum_value (double array[No_COMPANIES], int n)
{
    return 0.0;
}