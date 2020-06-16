/*
 * Basic CDS curve bootstrapper. Script takes the CDS curve and calculates the risk-neutral survival probabilities.
 */

#include <iostream>
#include <cmath>
using namespace std;

//Function prototypes here.
void bond_curve_bootstrapper (double zero_disc_factor[6]);
double bond_price_from_yield (double yield, double coupon_rate, double par_value, int bond_maturity);
void cds_curve_bootstrapper ();

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
    //Bootstrapp cds curve.
    cds_curve_bootstrapper();

    return 0;
}

void cds_curve_bootstrapper ()
{
/*
Function to perform bootstrapping of cds curve from data available in the market.
*/
    // Create array to carry the information of cds contracts to be bootstrapped.
    cds_contract cds_info[5];
    cds_info[0] = {"1Y cds", 100, 1.0};
    cds_info[1] = {"2Y cds", 114.00, 2.0};
    cds_info[2] = {"3Y cds", 121.0, 3};
    cds_info[3] = {"4Y cds", 135.0, 4};
    cds_info[4] = {"5Y cds", 145.0, 5.0};

    //Obtain the bootstrapped zero yields from bonds' prices.
    double risk_free_df[6];
    bond_curve_bootstrapper(risk_free_df); //function to bootstrapp bond curve.

    //Initialize useful variable.
    double survival_probability[6];
    double LGD = 0.4;  // discount factor for the risk free lender. 
    int index;

    //Initialize array with 1s.
    for (index = 0; index < 6; index++)
    {
        survival_probability[index] = 1.0;
    }

    //Begin bootstrapping here.
    //First calculate the 1st implied survival probability.
    survival_probability[1] = LGD/(LGD + cds_info[0].cds_spread/pow(10, 4));
    //cout << cds_info[0].cds_name + " survival probability\n" << survival_probability[0] << endl;

    //Then calculate the 2nd, 3rd etc...
    for (index = 2; index < 6; index++)
    {
        double temp_calc = 0;  //Variable to store summation. Only needed in this scope.
        int inner_index;

        for (inner_index = 1; inner_index < index; inner_index++)
        {
            temp_calc += risk_free_df[inner_index + 1]*(LGD*survival_probability[inner_index - 1] - (LGD + cds_info[inner_index].cds_spread/pow(10, 4))*survival_probability[inner_index]);
        }
        cout << "summation " << temp_calc << endl;

        //spreads are divived by 10^4 for conversion to %.
        survival_probability[index] = temp_calc/(risk_free_df[index + 1]*(LGD + cds_info[index].cds_spread/pow(10, 4))) + survival_probability[index - 1]*LGD/(LGD + cds_info[index].cds_spread/pow(10, 4)); 
    }

    for (index = 1; index < 6; index++)
    {
        cout << cds_info[index - 1].cds_name + " survival probability\n" << survival_probability[index] << endl;
    }
}

void bond_curve_bootstrapper (double zero_disc_factor[6])
{
/*
Function to perform bootstrapping of coupon bearing bonds from data available in the market.
*/
    // Create array to carry the information of bonds to be bootstrapped.
    coupon_bonds bonds_info[5];
    //bonds_info[0] = {"6m bond", 0.00185, 0.0, 0.5};
    bonds_info[0] = {"1Y bond", 0.00183, 0.0, 1.0};
    bonds_info[1] = {"2Y bond", 0.00199, 0.001, 2.0};
    bonds_info[2] = {"3Y bond", 0.00232, 0.0012, 3};
    bonds_info[3] = {"4Y bond", 0.00236, 0.0015, 4};
    bonds_info[4] = {"5Y bond", 0.00342, 0.0014, 5.0};

    //Initialize useful variable.
    
    int index;

    //Initialize element 0 for zero_disc_factor array.
    zero_disc_factor[0] = 0.0;

    //Begin the bootstrapp here.
    for (index = 1; index < 6; index++)
    {
        double current_bond_price = bond_price_from_yield(bonds_info[index - 1].yield, bonds_info[index - 1].coupon, 1.0, bonds_info[index - 1].maturity);
        double temp_factor = 0;

        cout << bonds_info[index - 1].bond_name + " price\n";
        cout << current_bond_price << endl; 

        int inner_index;
        for (inner_index = 0; inner_index < index; inner_index++)
        {
            temp_factor += zero_disc_factor[inner_index]*bonds_info[inner_index].coupon;
        }

        zero_disc_factor[index] = (current_bond_price - temp_factor)/(bonds_info[index - 1].coupon + 1);  //Face value is one for now.

        cout << bonds_info[index - 1].bond_name + " zero factor\n" << zero_disc_factor[index] << endl;
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
