#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;
using namespace std;

int main() 
{
    vector<double> x(5); x = {1, 2, 1, 2};

    plt::plot(x);
    plt::show();
}