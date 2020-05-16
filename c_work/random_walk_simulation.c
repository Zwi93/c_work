/* Script to model a binomial random walk using the in-built C function rand. */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define SPOT_PRICE 100
#define STRIKE 100
#define TRIALS 12
#define RATE 0.05
#define VOLATILITY 0.2
#define EXPIRY 1.0
#define STEPS 2000
#define TIME_STEP EXPIRY/STEPS
#define SIMULATIONS 100

double generate_normal_random_number (int no_of_trials);
void simulate_random_walk (double *array, int underlying_steps, int no_of_trials, double rate, double vol, double time_step, double spot_price);
void write_to_file (double *array, size_t object_size, size_t object_amount, char *filename);
void write_to_gnuplot (double *, int, FILE *gnuplotPipe);
void simulate_many_random_walks (int no_of_simulation, double *array, int underlying_steps, int no_of_trials, double rate, double vol, double time_step, double spot_price);
double normal_cdf (double x_param);
double vanilla_payoff_function (double stock_price, double strike, char type);
double monte_carlo_estimate (int no_of_simulation, double *array, int underlying_steps, int no_of_trials, double rate, double vol, double time_step, double spot_price, double strike);
void comparison_to_exact (double *array, int underlying_steps, int no_of_trials, double rate, double vol, double time_step, double spot_price, double strike);
double binary_payoff_function (double stock_price, double strike, char type);

int main ()
{
    double random_walk_array[STEPS];
    //int index;
    //char *filename = "random_walk_simulation.dat";
    //size_t object_size = sizeof(int);
    //size_t object_amount = (size_t) STEPS;
    
    double option_estimate;
    clock_t begin = clock();
    //simulate_many_random_walks (SIMULATIONS, random_walk_array, STEPS, TRIALS, RATE, VOLATILITY, TIME_STEP, SPOT_PRICE);
    //option_estimate = monte_carlo_estimate (SIMULATIONS, random_walk_array, STEPS, TRIALS, RATE, VOLATILITY, TIME_STEP, SPOT_PRICE, STRIKE);
    //printf("Monte Carlo Estimate: %f\n", option_estimate);
    comparison_to_exact(random_walk_array, STEPS, TRIALS, RATE, VOLATILITY, TIME_STEP, SPOT_PRICE, STRIKE);
    clock_t end = clock();
    double time_spent = (double) (end - begin)/CLOCKS_PER_SEC;
    printf("Elapsed time: %f\n", time_spent);

    //Write to Gnuplot.
    //write_to_gnuplot (random_walk_array, STEPS);
    
    //write_to_file (random_walk_array, object_size, object_amount, filename);
    return 0;
}

double generate_normal_random_number (int no_of_trials)
{
    //no_of_trials is the number of times the experiment is perfomed; any integer number will do but the higher the more accurate the random number to normal.
    int index;
    double random_number = 0;
    double uniform_rv;
    
    
    for (index = 0; index < no_of_trials; index++)
    {
        uniform_rv = ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
        random_number += uniform_rv;
    }

    random_number = sqrt(12/no_of_trials)*(random_number - no_of_trials/2);

    return random_number;
}

void simulate_random_walk (double *array, int size_of_array, int no_of_trials, double rate, double vol, double time_step, double spot_price)
{
    int index;

    array[0] = spot_price;
    
    for (index = 1; index < size_of_array; index++)
    {    
        array[index] = array[index - 1]*(1 + rate*time_step + vol*generate_normal_random_number(no_of_trials)*sqrt(time_step)); 
    }
}

void write_to_file (double *array, size_t object_size, size_t object_amount, char *filename)
{
    FILE *my_stream;
    my_stream = fopen(filename, "w");

    size_t op_return;
    op_return = fwrite(&array, object_size, object_amount, my_stream);
    if (op_return != object_amount)
    {
        printf ("Error writing data to file.\n");
    }
    else
    {
        printf ("Writing data succcessful!\n");
    }
    fclose(my_stream);
}

void write_to_gnuplot (double *array, int size_of_array, FILE *gnuplotPipe)
{

    int index;
    for (index = 0; index < size_of_array; index++)
    {
        fprintf (gnuplotPipe, "%d %f\n", index, array[index]);
    }
    
}

void simulate_many_random_walks (int no_of_simulation, double *array, int size_of_array, int no_of_trials, double rate, double vol, double time_step, double spot_price)
{
    //Function to simulate the paths taken by the underlying under the log-normal assumption. Plots are also produced through the gnuplot stream.

    FILE *gnuplotPipe = popen("gnuplot", "w");

    fprintf(gnuplotPipe, "set terminal pngcairo\n");
    fprintf(gnuplotPipe, "set output 'test.png\n");
    fprintf(gnuplotPipe, "set xrange[-1:]\n");
    fprintf(gnuplotPipe, "set yrange[-1:]\n");
    fprintf(gnuplotPipe, "set title 'Stock Paths under Log-normal walk'\n");
    fprintf(gnuplotPipe, "set xlabel 'Steps'\n");
    fprintf(gnuplotPipe, "set ylabel 'Stock Price'\n");
    fprintf(gnuplotPipe, "set style data dots\n");
    fprintf(gnuplotPipe, "plot '-'\n");

    int index;
    srand(time(NULL));
    for (index = 0; index < no_of_simulation; index++)
    {
        simulate_random_walk (array, size_of_array, no_of_trials, rate, vol, time_step, spot_price);
        write_to_gnuplot (array, size_of_array, gnuplotPipe);
        
    }

    fprintf(gnuplotPipe, "e\n");
    fflush(gnuplotPipe);
}

double monte_carlo_estimate (int no_of_simulation, double *array, int size_of_array, int no_of_trials, double rate, double vol, double time_step, double spot_price, double strike)
{
    int index;
    double estimate = 0;
    srand(time(NULL));
    for (index = 0; index < no_of_simulation; index++)
    {
        double payoff;
        simulate_random_walk (array, size_of_array, no_of_trials, rate, vol, time_step, spot_price);
        payoff = binary_payoff_function(array[size_of_array - 1], strike, 'C');
        estimate += payoff;
    }

    estimate = estimate/no_of_simulation;

    double expiry, discounted_estimate;

    expiry = time_step*size_of_array;
    discounted_estimate = exp(-rate*expiry)*estimate;

    return discounted_estimate;
}

void comparison_to_exact (double *array, int size_of_array, int no_of_trials, double rate, double vol, double time_step, double spot_price, double strike)
{
    //Function to compare the estimate of the monte carlo scheme to the exact solution of the option; and plot the results.

    FILE *gnuplotPipe = popen("gnuplot", "w");

    fprintf(gnuplotPipe, "set terminal pngcairo\n");
    fprintf(gnuplotPipe, "set output 'test2.png\n");
    fprintf(gnuplotPipe, "set xrange[0:]\n");
    fprintf(gnuplotPipe, "set yrange[0:1]\n");
    fprintf(gnuplotPipe, "set title 'Monte Carlo Estimate vs Exact Price'\n");
    fprintf(gnuplotPipe, "set xlabel 'No. of Simulations'\n");
    fprintf(gnuplotPipe, "set ylabel 'Option Price'\n");
    //fprintf(gnuplotPipe, "plot %f\n", 0.532325);
    //fprintf(gnuplotPipe, "set style data dots\n");
    fprintf(gnuplotPipe, "plot '-'\n");


    int index;
    for (index = 0; index < 100; index++)
    {
        int simulation_size;
        simulation_size = 100 + 100*index;
        double corresponding_estimate;
        corresponding_estimate = monte_carlo_estimate (simulation_size, array, size_of_array, no_of_trials, rate, vol, time_step, spot_price, strike);
        fprintf (gnuplotPipe, "%d %f\n", simulation_size, corresponding_estimate);
    }

    fprintf(gnuplotPipe, "e\n");
    //fprintf(gnuplotPipe, "plot %f\n", 0.532325);
    fflush(gnuplotPipe);

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

double normal_cdf (double x_param)
{
    double normal_cdf;
    double new_param = x_param/sqrt(2);

    normal_cdf = 0.5 + 0.5*erf(new_param);

    return normal_cdf;
}