/*
 * Basic coupon bond curve bootstrapper. Script takes the bond curve and calculates the zero- coupon yields..
 */

 #include <iostream>
 #include <string>
 #include <cmath>
 using namespace std;

// define struct type to hold info about bonds.
struct coupon_bonds 
{
    string bond_name;
    float yield;
    float coupon;
}

int main ()
{
    // Initiate object of type coupon_bonds.
    coupon_bonds y1_bond = {"1Y bond", 0.15, 0.05};
    double bond_price = exp(-y1_bond.yield*1.0);
    cout << "Bond's price is: " << bond_price << endl;
    return 0;
}