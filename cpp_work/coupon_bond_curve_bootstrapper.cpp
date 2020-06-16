/*
 * Basic coupon bond curve bootstrapper. Script takes the bond curve and calculates the zero- coupon yields..
 */

 #include <iostream>
 #include <string>
 #include <cmath>
 using namespace std;

//Function prototypes come here.
double price_from_yield (double yield, double coupon_rate, double par_value, int bond_maturity);
void bond_curve_bootstrapper (double zero_disc_factor[6]);

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
    // Perform the bootstrapping. 
    double zero_disc_factor[6];
    bond_curve_bootstrapper (zero_disc_factor);
    return 0;
};

double price_from_yield (double yield, double coupon_rate, double par_value, int bond_maturity)
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
        double current_bond_price = price_from_yield(bonds_info[index - 1].yield, bonds_info[index - 1].coupon, 1.0, bonds_info[index - 1].maturity);
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