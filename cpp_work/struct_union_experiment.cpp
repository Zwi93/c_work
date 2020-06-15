/*
 * Script to experiment on the struct and union data types of C++.
*/

#include <iostream>
using namespace std;

union value 
{
    long int i_value;  // The real number.
    float f_value;   // The floating point number.
};

struct struct_value
{
    long int i_value;  // The real number.
    float f_value;    // The float number.
};

int main ()
{
    // Initialize variable of type value.
    value data;
    data.i_value = 1;
    cout << "Results from union data type\n";
    cout << data.i_value << endl;
    data.f_value = 5.0;
    cout << data.f_value << endl;

    // Intialize variable of type struct_value.
    struct_value struct_data = {2, 2.3};
    cout << "Results from struct data type\n";
    cout << struct_data.i_value << endl;
    cout <<  struct_data.f_value << endl;
    return 0;
}