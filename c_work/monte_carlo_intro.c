/* Module for the construction of the monte carlo method for basic integrals. */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define TRIALS 1000000

double monte_carlo_estimate (int no_of_trials);

int main ()
{
    double *ptr_estimator;
    ptr_estimator = (double*) malloc (sizeof(double));
    *ptr_estimator = monte_carlo_estimate(TRIALS);
    //double estimation = monte_carlo_estimate(TRIALS);
    printf("Estimated : %f\n", *ptr_estimator);
    printf("Exact : %f\n", (sqrt(M_PI)/2)*erf(1));
    free(ptr_estimator);
    
    return 0;
}

double monte_carlo_estimate (int no_of_trials)
{
    //Generate uniformly distributed random numbers in the range (0, 1) and then compute the corresponding monte_carlo estimate.
    double uniform_rv;
    double estimator = 0;

    int index;
    for (index = 0; index < no_of_trials; index++)
    {
        uniform_rv = ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
        estimator += exp(-uniform_rv*uniform_rv); 
    }
    return estimator/no_of_trials;
}