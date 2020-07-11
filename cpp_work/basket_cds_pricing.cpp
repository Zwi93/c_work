/************************************************************************************************************************************
 * Purpose: Given the correlation matrix one can price the fair spread of a nth-to-default basket CDS using functions defined here. * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Usage: Provide the correlation matrix and the script will compute the fair basket spread.                                        *
 *                                                                                                                                  *
 ************************************************************************************************************************************
 */

//Include all relevant header files here.
#include "cds_curve_bootstrapper.h"
#include "matplotlibcpp.h"

using namespace std;
namespace plt = matplotlibcpp;

int main ()
{   
    //Creeate a 5 by 6 array to hold all these credit curves.
    contract_info cds_curves_matrix[No_COMPANIES][6];

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[0][0] = {"0.5Y cds", 9.5, 0.0, 0.5};
    cds_curves_matrix[0][1] = {"1Y cds", 10.00, 0.0, 1.0};
    cds_curves_matrix[0][2] = {"2Y cds", 14.700, 0.0, 2.0};
    cds_curves_matrix[0][3] = {"3Y cds", 21.890, 0.0, 3};
    cds_curves_matrix[0][4] = {"4Y cds", 25.500, 0.0, 4};
    cds_curves_matrix[0][5] = {"5Y cds", 29.406, 0.0, 5.0};

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[1][0] = {"0.5Y cds", 11.132, 0.0, 0.5};
    cds_curves_matrix[1][1] = {"1Y cds", 17.560, 0.0, 1.0};
    cds_curves_matrix[1][2] = {"2Y cds", 24.410, 0.0, 2.0};
    cds_curves_matrix[1][3] = {"3Y cds", 29.980, 0.0, 3};
    cds_curves_matrix[1][4] = {"4Y cds", 36.780, 0.0, 4};
    cds_curves_matrix[1][5] = {"5Y cds", 41.431, 0.0, 5.0};

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[2][0] = {"0.5Y cds", 25.452, 0.0, 0.5};
    cds_curves_matrix[2][1] = {"1Y cds", 30.741, 0.0, 1.0};
    cds_curves_matrix[2][2] = {"2Y cds", 34.000, 0.0, 2.0};
    cds_curves_matrix[2][3] = {"3Y cds", 35.651, 0.0, 3};
    cds_curves_matrix[2][4] = {"4Y cds", 45.347, 0.0, 4};
    cds_curves_matrix[2][5] = {"5Y cds", 52.495, 0.0, 5.0};

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[3][0] = {"0.5Y cds", 314.451, 0.0, 0.5};
    cds_curves_matrix[3][1] = {"1Y cds", 374.145, 0.0, 1.0};
    cds_curves_matrix[3][2] = {"2Y cds", 405.521, 0.0, 2.0};
    cds_curves_matrix[3][3] = {"3Y cds", 450.874, 0.0, 3};
    cds_curves_matrix[3][4] = {"4Y cds", 489.417, 0.0, 4};
    cds_curves_matrix[3][5] = {"5Y cds", 519.097, 0.0, 5.0};

    // Create array of struct type (cds_contract) to carry the information of cds contracts to be bootstrapped.
    cds_curves_matrix[4][0] = {"0.5Y cds", 17.63, 0.0, 0.5};
    cds_curves_matrix[4][1] = {"1Y cds", 21.21, 0.0, 1.0};
    cds_curves_matrix[4][2] = {"2Y cds", 28.41, 0.0, 2.0};
    cds_curves_matrix[4][3] = {"3Y cds", 31.85, 0.0, 3};
    cds_curves_matrix[4][4] = {"4Y cds", 26.78, 0.0, 4};
    cds_curves_matrix[4][5] = {"5Y cds", 30.97, 0.0, 5.0};


    double LGD = 0.4; //Loss Given Default, assumed constant and equal for each company.
    int n = 1; //Contract defaulting type, i.e 1st, 2nd, etc to default.

    //basket_cds_mc_pricing_adjusted(No_COMPANIES, SIMULATIONS, 0, cds_curves_matrix, LGD, n, MATURITY, "gaussian");
    basket_cds_mc_pricing(No_COMPANIES, SIMULATIONS, 0, cds_curves_matrix, LGD, n, MATURITY, "gaussian");

    //double nth_minimum_value = get_nth_minimum_value(array, n);

    //cout << n << " Min " << nth_minimum_value << endl;
    //double t_dist = student_t_cdf(0.5, 3);
    //double check = 0.5 + ((1/sqrt(3))*(0.5/(1 + 0.5*0.5/3)) + atan(0.5/sqrt(3)))/MY_PI;
    //double beta_inc = incomplete_beta_function1();

    //cout << "t value " << t_dist << " and tan value " << check << endl;
    //cout << "Beta-incomplete " << beta_inc << endl;

    return 0;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the spread for the basket cds using a faster monte carlo technique.                                 *
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * no_of_credits is the basket's number of underlyings, no_of_simulations is how many monte carlo simulation to perform, order is   *
 * parameter to manage the accuracy of the inverse_default_cdf, cds_curve_matrix variable contains all the data for each underlying *
 * nth_default determines which type of CDS it is, 1st, 2nd, etc, and maturity is the contract's maturity.                          *
 *                                                                                                                                  *
 * Return: This is a void function.                                                                                                 *
 ************************************************************************************************************************************
 */
void basket_cds_mc_pricing_adjusted (int no_of_credits, int no_of_simulations, int order, contract_info cds_curves_matrix[No_COMPANIES][6], double LGD, int nth_default, double maturity, string copula_type)
{
    int index;
    double fair_spread = 0, premium_leg = 0, protection_leg = 0; //Rolling average spread to be saved here.

    for (index = 0; index < no_of_simulations; index++)
    {
        int inner_index, count_defaults = 0; double independent_normal_rvs[no_of_credits];  //Array to store independent normal variates.
        double payoff_adjustment = 1; //Keep track of number of defaults and adjustment to payoff.
        double correlation_matrix0[No_COMPANIES][No_COMPANIES], pseudo_matrix0[No_COMPANIES][No_COMPANIES]; //Matrix to store correlation matrix and its Cholesky Decomposition. 

        //Populate independent_normal_rvs by zeros.
        int temp_i;
        for (temp_i = 0; temp_i < no_of_credits; temp_i++)
        {
            independent_normal_rvs[temp_i] = 0.0;
        }
        
        //Get the correlation matrix and store in variable correlation_matrix and compute the cholesky decomposition.
        get_correlation_matrix(correlation_matrix0, copula_type);
        get_pseudo_square_root(correlation_matrix0, pseudo_matrix0); 

        //Case of inner_index = 0 has to be handled separately. 
        double first_rv = ((double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
        contract_info first_cds_info[6];
        int i;
        for (i = 0; i < 6;i++)
        {
            first_cds_info[i] = cds_curves_matrix[0][i];
        } 
        double first_survival_probability[11];double delta_t = 0.5;
        
        cds_curve_bootstrapper(first_survival_probability, first_cds_info, LGD);int index_maturity = floor(maturity/delta_t);
        
        double first_bound = inverse_normal_cdf(order, 1 - first_survival_probability[index_maturity]);
        double first_uncorrelated_bound = normal_cdf(first_bound);
        double numerator0 = nth_default; double adjusted_prob0 = numerator0/No_COMPANIES; 

        
        if (first_rv < adjusted_prob0)
        {
            double first_uncorrelated_normal = inverse_normal_cdf(order ,first_uncorrelated_bound*first_rv/adjusted_prob0);
            independent_normal_rvs[0] = first_uncorrelated_normal;
            count_defaults += 1;
            payoff_adjustment *= first_uncorrelated_bound/adjusted_prob0;
        }
        if (first_rv > adjusted_prob0)
        {
            double v_1 = first_uncorrelated_bound + (1 - first_uncorrelated_bound)*(first_rv - adjusted_prob0)/(1 - adjusted_prob0);
            independent_normal_rvs[0] = inverse_normal_cdf(order, v_1);
            count_defaults += 0;
            payoff_adjustment *= (1 - first_uncorrelated_bound)/(1 - adjusted_prob0);
        }
        
        //Obtain pseudo random numbers in the range (0, 1) and corresponding adjusted normal variates.
        //Loop is going over each credit in the basket.
        for (inner_index = 1; inner_index < no_of_credits; inner_index++)
        {
            double correlated_normal_bound; //Normals below this value will guaranttee a default.
            double survival_probability0[11];
            double adjusted_default_prob; //With this prob, default is guaruanteed to occur in each simulation path.
            
            if (nth_default == 1)
            {
                adjusted_default_prob = 1.0/(No_COMPANIES - inner_index);
            }
            else
            {
                double numerator = nth_default - count_defaults;
                if (inner_index == No_COMPANIES - 2)
                {
                    adjusted_default_prob = numerator/1.0;
                }
                else
                {
                    adjusted_default_prob = numerator/(No_COMPANIES -(inner_index + 1 + 1));
                }
            }

            
            //Now draw a pseudo uniform RV.
            double pseudo_uniform_rv = ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
            
            //Construct the credit curves fo each counterpart.
            contract_info cds_info[6];

            int tenor_index; //The tenor of the curve point.
            for (tenor_index = 0; tenor_index < 6; tenor_index++)
            {
                cds_info[tenor_index] = cds_curves_matrix[inner_index][tenor_index];
            }
        
            //Obtain the survival probabilities for counterpart corresponding to index inner_index.
            cds_curve_bootstrapper(survival_probability0, cds_info, LGD);

            double delta_t = 0.5; int index_maturity = floor(maturity/delta_t);

            //Obtain the limiting value to guarantee default in the simulation path.
            correlated_normal_bound = inverse_normal_cdf(order, 1 - survival_probability0[index_maturity]);
            
            //Decide whether enough defaults have occured.

            if (adjusted_default_prob > 0)
            {
                double temp_sum = 0; //Needed for the calculation of new updated uniform.
                double updated_uniform, uncorrelated_normal_bound;

                int inner_inner_i;

                for (inner_inner_i = 0; inner_inner_i < inner_index; inner_inner_i++)
                {
                    //cout << "factors in the sum " << pseudo_matrix0[inner_index][inner_inner_i] << endl;
                    //cout << "factors in the sum " << independent_normal_rvs[inner_inner_i] << endl;
                    temp_sum += pseudo_matrix0[inner_index][inner_inner_i]*independent_normal_rvs[inner_inner_i];
                }

                //cout << "Temporary Sum " << temp_sum << endl;
                uncorrelated_normal_bound = (correlated_normal_bound - temp_sum)/pseudo_matrix0[inner_index][inner_index];
                uncorrelated_normal_bound = normal_cdf(uncorrelated_normal_bound);
                //cout << "Uncorrelated Normal Boundary, i.e p " << uncorrelated_normal_bound << endl;

                //cout << "Pseudo uniform output " << pseudo_uniform_rv << endl;
                //cout << "adjusted probability of default to guaruantee default " << adjusted_default_prob << endl;

                //Examine condition of guarauntteed default and adjust quantities accordingly.
                if (pseudo_uniform_rv < adjusted_default_prob)
                {
                    updated_uniform = uncorrelated_normal_bound*pseudo_uniform_rv/adjusted_default_prob;
                    //cout << "Updated uniform RVS " << updated_uniform << endl;
                    double calculated_normal = inverse_normal_cdf(order, updated_uniform);
                    //cout << "Calculation of independent normal from updated uniform " << calculated_normal << endl;
                    independent_normal_rvs[inner_index] = inverse_normal_cdf(order, updated_uniform);
                    count_defaults += 1;
                    payoff_adjustment *= uncorrelated_normal_bound/adjusted_default_prob;
                }

                else 
                {
                    updated_uniform = uncorrelated_normal_bound + (1 - uncorrelated_normal_bound)*(pseudo_uniform_rv - adjusted_default_prob)/(1 - adjusted_default_prob);
                    //cout << "Updated uniform RVS " << updated_uniform << endl;

                    double calculated_normal = inverse_normal_cdf(order, updated_uniform);
                    //cout << "Calculation of independent normal from updated uniform " << calculated_normal << endl;
                    independent_normal_rvs[inner_index] = inverse_normal_cdf(order, updated_uniform);
                    count_defaults += 0;
                    payoff_adjustment *= (1 - uncorrelated_normal_bound)/(1 - adjusted_default_prob);
                }
            }

            else 
            {
                independent_normal_rvs[inner_index] = inverse_normal_cdf(order, pseudo_uniform_rv);
            }

        }

        
        //Convert the 1d normals array to 2d;matrix product function can only handle square matrix, not vector.
        double independent_normal_rvs_matrix[No_COMPANIES][No_COMPANIES];
        one_to_many_dimension(independent_normal_rvs, independent_normal_rvs_matrix);

        //Arrays to store the correlation matrix, pseudo-square-root, and finally from these two obtain the correlated normals matrix (or vector).
        double correlated_normals[No_COMPANIES][No_COMPANIES], correlation_matrix[No_COMPANIES][No_COMPANIES], pseudo_matrix[No_COMPANIES][No_COMPANIES];

        if (copula_type == "gaussian")
        {
            //Get the correlation matrix and store in variable correlation_matrix and compute the cholesky decomposition.
            get_correlation_matrix(correlation_matrix, copula_type);
            get_pseudo_square_root(correlation_matrix, pseudo_matrix);

            //Get the correlated normal RVs;the values are stored in the 1st column.
            matrix_product(pseudo_matrix, independent_normal_rvs_matrix, correlated_normals, 1.0);
        }

        int mu = 3; //Mu parameter for the chi squared and student t distributions.
        if (copula_type == "t_stat")
        {
            //Get the correlation matrix and store in variable correlation_matrix and compute the cholesky decomposition.
            get_correlation_matrix(correlation_matrix, copula_type);
            get_pseudo_square_root(correlation_matrix, pseudo_matrix);

            //Get the chi squared RVs from its definition as the sum of squares of normal RVs. 
            int count_mu;
            double chi_squared_rv = 0;
            
            for (count_mu = 0; count_mu < mu; count_mu++)
            {
                double normal_rv, uniform_rv;
                uniform_rv = ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
                normal_rv = inverse_normal_cdf(order, uniform_rv);
                chi_squared_rv += normal_rv*normal_rv; 
            }

            double multiplication_factor; //Factor going in the matrix product calcs.
            multiplication_factor = sqrt(mu/chi_squared_rv);

            //Get the correlated normal RVs;the values are stored in the 1st column.
            matrix_product(pseudo_matrix, independent_normal_rvs_matrix, correlated_normals, multiplication_factor);
            
        }



        double correlated_default_times[No_COMPANIES]; //Variable to store the correlated default time for each credit.
        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            double correlated_uniform_rv;

            /*Uniform variates will differ depending on the type of copula method; the gaussian copula uses the relevant gaussian copula marginal cdf, and the 
            student's t copula uses its own relevant t marginal cdf. This is handled in the if statements below.*/
            
            if (copula_type == "gaussian")
            {
                //cout << "Correlated normal for credit " << inner_index << endl; cout << correlated_normals[inner_index][0] << endl;
                correlated_uniform_rv = normal_cdf(correlated_normals[inner_index][0]);
            }
            if (copula_type == "t_stat")
            {
                correlated_uniform_rv = student_t_cdf(correlated_normals[inner_index][0], mu);
            }

            //cout << "Correlated uniform RVs for credit " << inner_index << endl;cout << correlated_uniform_rv << endl;

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

            //cout << "Minimum Survival probability " << survival_probability[10] << endl;
            //cout << "Maximum Survival probability " << survival_probability[1] << endl;

            //Next from the survival probabilities, get the hazard rates.
            double hazard_rates[11];
            get_hazard_rates(survival_probability, hazard_rates);
            
            //Then obtain the correlated default time.
            correlated_default_times[inner_index] = survival_time_inverse_cdf(hazard_rates, 1 - correlated_uniform_rv, 1000, 0.001);

            //cout << "Correlated default time for Counterpart " << inner_index << " " << correlated_default_times[inner_index] << endl;
        }

        //Next determine the 1st, 2nd, etc default time, depending on the nth_default input value.
        double nth_default_time; //time of default variable;depends on the input nth_default integer.

        nth_default_time = get_nth_minimum_value(correlated_default_times, nth_default);

        //cout << "Nth default time for Contract " << nth_default_time << endl;

        //Determine the fair spread based on this nth default time and the zero discount factors are also important for this purpose.
        double zero_disc_factors[11];
        bond_curve_bootstrapper(zero_disc_factors);
        
        //cout << "Loop no. " << index << endl;
        int lower_bound = floor(nth_default_time/delta_t);
        double payoff_legs[2];
        //cout << "Lower bound " << lower_bound << endl;
        fair_spread += premium_protection_leg_calcs(nth_default_time, maturity, LGD, delta_t, zero_disc_factors, payoff_legs);
        premium_leg += payoff_adjustment*payoff_legs[1]; protection_leg += payoff_adjustment*payoff_legs[0];

        cout << "Default time " << nth_default_time << endl;
    }

    double average_fair_spread1 = fair_spread/no_of_simulations, average_fair_spread2 = protection_leg/premium_leg;

    cout << "Real Average Spread (adjusted MC)" << average_fair_spread2 << endl; 
    
} 

/************************************************************************************************************************************
 * Purpose: Function to compute the spread for the basket cds using monte carlo techniques.                                         * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * no_of_credits is the basket's number of underlyings, no_of_simulations is how many monte carlo simulation to perform, order is   *
 * parameter to manage the accuracy of the inverse_default_cdf, cds_curve_matrix variable contains all the data for each underlying *
 * nth_default determines which type of CDS it is, 1st, 2nd, etc, and maturity is the contract's maturity.                          *
 *                                                                                                                                  *
 * Return: This is a void function.                                                                                                 *                                                                                                                                  
 ************************************************************************************************************************************
 */
void basket_cds_mc_pricing (int no_of_credits, int no_of_simulations, int order, contract_info cds_curves_matrix[No_COMPANIES][6], double LGD, int nth_default, double maturity, string copula_type)
{
    int index;
    double fair_spread = 0, premium_leg = 0, protection_leg = 0; //Rolling average spread to be saved here.
    vector<double> fair_spread_path(no_of_simulations);

    for (index = 0; index < no_of_simulations; index++)
    {
        int inner_index; double uniform_rvs[no_of_credits];  //Array to store univariates.

        //Obtain pseudo random numbers in the range (0, 1).
        for (inner_index = 0; inner_index < no_of_credits; inner_index++)
        {
            uniform_rvs[inner_index] = ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
        }

        double normal_rvs[No_COMPANIES], normal_rvs_matrix[No_COMPANIES][No_COMPANIES]; // Array to store corresponding uncorrelated normals.

        //Obtain corresponding standard normal variables from the uniforms.
        for (inner_index = 0; inner_index < no_of_credits; inner_index++)
        {
            normal_rvs[inner_index] = inverse_normal_cdf(order, uniform_rvs[inner_index]);
        }
        
        //Convert the 1d normals array to 2d;matrix product function can only handle square matrix, not vector.
        one_to_many_dimension(normal_rvs, normal_rvs_matrix);

        //Arrays to store the correlation matrix, pseudo-square-root, and finally from these two obtain the correlated normals matrix (or vector).
        double correlated_normals[No_COMPANIES][No_COMPANIES], correlation_matrix[No_COMPANIES][No_COMPANIES], pseudo_matrix[No_COMPANIES][No_COMPANIES];

        if (copula_type == "gaussian")
        {
            //Get the correlation matrix and store in variable correlation_matrix and compute the cholesky decomposition.
            get_correlation_matrix(correlation_matrix, copula_type);
            get_pseudo_square_root(correlation_matrix, pseudo_matrix);

            //Get the correlated normal RVs;the values are stored in the 1st column.
            matrix_product(pseudo_matrix, normal_rvs_matrix, correlated_normals, 1.0);
        }

        int mu = 3; //Mu parameter for the chi squared and student t distributions.
        if (copula_type == "t_stat")
        {
            //Get the correlation matrix and store in variable correlation_matrix and compute the cholesky decomposition.
            get_correlation_matrix(correlation_matrix, copula_type);
            get_pseudo_square_root(correlation_matrix, pseudo_matrix);

            //Get the chi squared RVs from its definition as the sum of squares of normal RVs. 
            int count_mu;
            double chi_squared_rv = 0;
            
            for (count_mu = 0; count_mu < mu; count_mu++)
            {
                double normal_rv, uniform_rv;
                uniform_rv = ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
                normal_rv = inverse_normal_cdf(order, uniform_rv);
                chi_squared_rv += normal_rv*normal_rv; 
            }

            double multiplication_factor; //Factor going in the matrix product calcs.
            multiplication_factor = sqrt(mu/chi_squared_rv);

            //Get the correlated normal RVs;the values are stored in the 1st column.
            matrix_product(pseudo_matrix, normal_rvs_matrix, correlated_normals, multiplication_factor);
            
        }

        double correlated_default_times[No_COMPANIES]; //Variable to store the correlated default time for each credit.
        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            double correlated_uniform_rv;

            /*Uniform variates will differ depending on the type of copula method; the gaussian copula uses the relevant gaussian copula marginal cdf, and the 
            student's t copula uses its own relevant t marginal cdf. This is handled in the if statements below.*/
            
            if (copula_type == "gaussian")
            {
                correlated_uniform_rv = normal_cdf(correlated_normals[inner_index][0]);
            }
            if (copula_type == "t_stat")
            {
                correlated_uniform_rv = student_t_cdf(correlated_normals[inner_index][0], mu);
            }

            //cout << "Correlated univariates " << correlated_uniform_rv << endl;

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
            correlated_default_times[inner_index] = survival_time_inverse_cdf(hazard_rates, 1 - correlated_uniform_rv, 1000, 0.001);

            //cout << "Correlated default time for Counterpart " << inner_index << " " << correlated_default_times[inner_index] << endl;
        }

        //Next determine the 1st, 2nd, etc default time, depending on the nth_default input value.
        double nth_default_time; //time of default variable;depends on the input nth_default integer.

        nth_default_time = get_nth_minimum_value(correlated_default_times, nth_default);

        cout << "Nth default time for Contract " << nth_default_time << endl;

        //Determine the fair spread based on this nth default time and the zero discount factors are also important for this purpose.
        double zero_disc_factors[11], delta_t = 0.5;
        bond_curve_bootstrapper(zero_disc_factors);
        
        //cout << "Loop no. " << index << endl;
        int lower_bound = floor(nth_default_time/delta_t);
        //cout << "Lower bound " << lower_bound << endl;
        double payoff_legs[2];
        fair_spread += premium_protection_leg_calcs(nth_default_time, maturity, LGD, delta_t, zero_disc_factors, payoff_legs);
        premium_leg += payoff_legs[1]; protection_leg += payoff_legs[0]; 
        fair_spread_path.at(index) = protection_leg/premium_leg;
    }

    double average_fair_spread1 = fair_spread/no_of_simulations, average_fair_spread2 = protection_leg/premium_leg;

    //cout << "Average Spread 1 " << average_fair_spread1 << endl;
    cout << "Real Average Spread " << average_fair_spread2 << endl;

    plt::plot(fair_spread_path);
    plt::show();
}

/************************************************************************************************************************************
 * Purpose: Function to compute the net of the premiums and protection leg given the default time and maturity of contract.         * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * nth_default_time : Time of the nth default in the basket, calculated from joint ditribution.                                     *
 * maturity : Maturity of contract.                                                                                                 *
 * zero_disc_factor ; Bootstrapped zero discount factors from prevailing market bond prices.                                        *
 * Return: The fair spread is returnd for the given inputs.                                                                         *                                                                                                                                  
 ************************************************************************************************************************************
 */

double premium_protection_leg_calcs (double nth_default_time, double maturity, double LGD, double delta_t, double zero_disc_factor[11], double payoff_legs[2])
{
    double protection_leg = 0, premium_leg = 0, fair_spread;

    if (nth_default_time < maturity)
    {
        //Determine the time interval where default occurs.
        int index;
        int lower_bound = floor(nth_default_time/delta_t);

        if (lower_bound > 1)
        {
            for (index = 1; index < lower_bound; index++)
            {
                premium_leg += zero_disc_factor[index];
            }

            protection_leg = LGD*zero_disc_factor[lower_bound];
        }

        if (lower_bound <= 1)
        {
            premium_leg = (zero_disc_factor[0] + zero_disc_factor[1])/2;
            protection_leg = LGD*(zero_disc_factor[0] + zero_disc_factor[1])/2;
        }  
    }

    if (nth_default_time >= maturity)
    {
        int index;

        for (index = 1; index < 11; index++)
        {
            premium_leg += zero_disc_factor[index];
        }

        protection_leg = 0;
    }

    payoff_legs[0] = protection_leg;
    payoff_legs[1] = premium_leg;

    fair_spread = protection_leg/premium_leg;

    return fair_spread;
}
/************************************************************************************************************************************
 * Purpose: Function to compute the Cholesky decomposition for given correlation matrix.                                            * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * correlation_matrix: matrix storing information about the correlations of the variables;assumed to be positive definite.          *
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
 * Purpose: Function to compute the cummulative density function for normal RVs;coverts normal RVs to uniform RVs.                  * 
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
    if (order != 0)
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

/************************************************************************************************************************************
 * Purpose: Function to compute an approximation to the hypergeometric function using series; used to obtain the incomple beta F    * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * Order refers to the highest power of the polynomial in the series, x_variable is the independent variable we wish to compute the *
 * approximation at, and the other are just parameters of the function as can be obtained from literature.                          *
 * Return: This returns a number approximating the series.                                                                          *                                                                                                                                  
 ************************************************************************************************************************************
 */
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

/************************************************************************************************************************************
 * Purpose: Functions to compute the incomplete beta function from the (0)hypergeometrix function and (1)numerical integration.     * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * x_param: x_variable is the independent x value we wish to compute the function at, and the others are just parameters of the fun *
 * ction as found in the literature.                                                                                                *
 * Return: The return value is the incomplete beta function at this x point.                                                        *                                                                                                                                  
 ************************************************************************************************************************************
 */
long double incomplete_beta_function (double a_param, double b_param, double x_variable)
{
    long double beta_value;

    beta_value = pow(x_variable, a_param)*hypergeometric_function(95, a_param, 1 - b_param, a_param + 1, x_variable)/a_param;

    return beta_value;
}

double incomplete_beta_function1 (double a_param, double b_param, double x_variable)
{
    double intergration_approximation;
    intergration_approximation = simpson(0, x_variable, 10000, a_param, b_param);

    return intergration_approximation;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the beta function from the gamma function, which is built in the language.                          * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * x_param: a_param and b_param are the independent values we wish to compute the function at.                                      *
 *                                                                                                                                  *
 * Return: The return value is the beta function at this x point.                                                                   *                                                                                                                                  
 ************************************************************************************************************************************
 */
double beta_function (double a_param, double b_param)
{
    double beta_value;
    beta_value = tgamma(a_param)*tgamma(b_param)/tgamma(a_param + b_param);

    return beta_value;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the student's t cdf function from the two beta functions.                                           * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * x_param is the independent value we wish to compute the function at, mu is the degree of freedom of the chi squared function.    *
 *                                                                                                                                  *
 * Return: The return value is the beta function at this x point.                                                                   *                                                                                                                                  
 ************************************************************************************************************************************
 */
double student_t_cdf (double x_value, double mu)
{
    double cdf_t, incomplete_beta_param;

    incomplete_beta_param = mu/(mu + x_value*x_value);

    if (x_value < 0)
        cdf_t = incomplete_beta_function1(mu/2, 0.5, incomplete_beta_param)/(2*beta_function(mu/2, 0.5));
    if (x_value > 0)
        cdf_t = 1 - incomplete_beta_function1(mu/2, 0.5, incomplete_beta_param)/(2*beta_function(mu/2, 0.5));
    if (x_value == 0)
        cdf_t = 1;

    return cdf_t;
}

/************************************************************************************************************************************
 * Purpose: Function to be provided as the integrand in the simpson/trapeziodal function.                                           * 
 *                                                                                                                                  *
 * Author: This is code stripped from code in notes from Dr Riaz Ahmad.                                                                                                               *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * x is the independent value of the function, parameters a and b are exponents in the function of interest in this project; this is*
 * the integrand in the incomplete bet function.                                                                                    *
 * Return: The return value is the integrand's value at x.                                                                   *                                                                                                                                  
 ************************************************************************************************************************************
 */
double f(double x, double a, double b) 
// integrand definition
{ 
    /* 3 different functions to try - remove the comment command
    when using the function of interest */
    //double function=x*x; // this is the only line to change.
    // double function= 1.0/(sqrt(2*pi))*exp(-x*x/2.0);

    double function= pow(x, a - 1)*pow(1 - x, b - 1);
    
    return function;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the simpson's approximation to the definite integral.                                               * 
 *                                                                                                                                  *
 * Author: This is code stripped from code in notes from Dr Riaz Ahmad.                                                             *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * lower_bound is the integral's lower_limit, same applies for upper_bound, and no_steps determines how the interval of integration *
 * is divided, and parameters a and b will go into the integrand.                                                                   *
 * Return: The returned value is an approximation to the incomplete beta function.                                                  *                                                                                                                                  
 ************************************************************************************************************************************
 */
double simpson(double lower_bound, double upper_bound, double no_steps, double a, double b)
{
    double sum_even = 0.0;
    double sum_odd = 0.0;
    double step_size = (upper_bound - lower_bound)/no_steps;
    int index;
    
    for (int index = 1; index <= (no_steps - 1); index++)
    {
        double x = lower_bound + index*step_size;
        
        if (index %2 == 0)
        {
            sum_even += f(x, a, b);
        }
        else
        {
            sum_odd += f(x, a, b);
        }
    }

    //cout << "sum even " << sum_even << endl;
    //cout << "sum odd " << sum_odd << endl;

    double inner_pts = 4*(sum_odd) + 2*(sum_even);
    double f_x = step_size*(f(lower_bound, a, b) + inner_pts + f(upper_bound, a, b))/3.0;

    //cout << "SImmpsom integral " << f_x << endl;

    return f_x;
}

/************************************************************************************************************************************
 * Purpose: Function to compute the trapezoidal approximation to the definite integral.                                             *  
 *                                                                                                                                  *
 * Author: This is code stripped from code in notes from Dr Riaz Ahmad.                                                             *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 *                                                                                                                                  *
 * lower_bound is the integral's lower_limit, same applies for upper_bound, and no_steps determines how the interval of integration *
 * is divided, and parameters a and b will go into the integrand.                                                                   *
 * Return: The returned value is an approximation to the incomplete beta function.                                                  *                                                                                                                                                                                                                                                                    
 ************************************************************************************************************************************
 */
double trapezoidal (double lower_bound, double upper_bound, double no_steps, double a, double b)
{
    double sum = 0.0; int index;
    double step_size = (upper_bound - lower_bound)/no_steps;

    for (int index = 1; index <= (no_steps - 1); index++)
    {
        double x = lower_bound + index*step_size;
        sum += f(x, a, b);
    }

    double inner_pts = 2*sum;
    double f_x = 0.5*step_size*(f(lower_bound, a, b) + inner_pts + f(upper_bound, a, b));
    
    return f_x;
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
void get_correlation_matrix (double correlation_array[][No_COMPANIES], string copula_type)
{
    string command = "python3 correlation_calcs.py";  //Command to run on the shell.
    const char *c_command = command.c_str();
    system(c_command);
    string correlation_file;

    if (copula_type == "gaussian") 
        correlation_file = "correlation_matrix_gaussian.txt";
    if (copula_type == "t_stat")
        correlation_file = "correlation_matrix_t.txt";
    
    //Create stream to the file.
    ifstream stream_to_file(correlation_file);
    int index1, index2, outer_index = 0; string line;

    //Read from the text file saved from the python script execution.
    while (getline(stream_to_file, line)) 
    {
        string word;

        //Create stream to the string variable 'word'.
        istringstream string_stream (line);
        int inner_index = 0;

        //read string word by word, and convert the string to a float value.
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
    /*Function computes the product of 2 matrices array_one and array_two then stores the product in a new array product_array. The two matrices are 
    assumed to be 2d. Also at the same time, scalar multiplication is implemented.*/

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

    for (outer_index = 0; outer_index < No_COMPANIES; outer_index++)
    {
        for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
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

/************************************************************************************************************************************
 * Purpose: Function to bootstrapp the cds curve from given input data.                                                             * 
 *                                                                                                                                  *
 * Author: Zwi Mudau                                                                                                                *
 *                                                                                                                                  *
 * Parameters:                                                                                                                      *
 * survival-probability: Array to store the implied survival probabilities from the bootstrapp.                                     *
 * LGD : Loss given default value.                                                                                                  *
 * contract_info: array holding screenshot of daily cds_curve up to 5y maturity.                                                    *
 * Return: This is a void function.                                                                                                 *                                                                                                                                  
 ************************************************************************************************************************************
 */

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
 * Purpose: Function to bootstrapp the bond curve from given input data.                                                             * 
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
    double estimated_value;

    while (difference_variable1*difference_variable2 > 0 & index < 10)
    {
        index += 1;
        exponent_sum += hazard_rates[index]*time_interval;
        
        difference_variable1 = x_input - exp(-exponent_sum);

        difference_variable2 = x_input - exp(-exponent_sum -hazard_rates[index + 1]*time_interval);

    }

    //cout << "Difference2 " << difference_variable2 << endl; 

    //cout << "Index stopped at " << index << endl;
    //Interval of intercept.
    if (index < 10)
    {
        double lower_bound = index*time_interval, upper_bound = lower_bound + time_interval;

        //cout << "Lower bound is " << lower_bound << endl;

        //Pick many values in this interval and evaluate difference to input value.
        estimated_value = lower_bound;double difference_variable3 = 1, delta_time = time_interval/divisions;

        while (abs(difference_variable3) > accuracy_level & estimated_value < upper_bound)
        {
            estimated_value += delta_time;
            difference_variable3 = x_input - exp(-exponent_sum - hazard_rates[index + 1]*(estimated_value - lower_bound));
        }
    }

    if (index == 10)
    {
        if (x_input >= exp(-hazard_rates[1]*time_interval))
        {
            //cout << "This is where the x_input is close to 1 " << endl;
            estimated_value = time_interval*(1 - x_input)/(1 - exp(-hazard_rates[1]*time_interval));
        }
        else
        {
            estimated_value = 5.05;
        }        
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
            if (qoutient_array[inner_index] == (double) 1)
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
    return minimum_index;
}

double get_nth_minimum_value (double array[No_COMPANIES], int n)
{
    int outer_index, inner_index;
    double reduced_array[No_COMPANIES];
    double sum_of_entries = 0;
    double global_min_value = 0;

    for (outer_index = 0; outer_index < No_COMPANIES; outer_index++)
    {
        reduced_array[outer_index] = array[outer_index];
        sum_of_entries += abs(array[outer_index]);  
    }

    
    for (outer_index = 0; outer_index < n; outer_index++)
    {
        int min_index = (int) get_minimum_value(reduced_array);

        //cout << "Min index at " << outer_index << " time " << min_index << endl;

        /*for (inner_index = 0; inner_index < No_COMPANIES; inner_index++)
        {
            if (reduced_array[inner_index] == min_value)
            {
                reduced_array[inner_index] = (outer_index + 1)*sum_of_entries;
            }
        }*/
        
        global_min_value = reduced_array[min_index];
        
        reduced_array[min_index] = sum_of_entries;
        
    }

    return global_min_value;
}

