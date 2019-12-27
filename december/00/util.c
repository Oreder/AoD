#include "util.h"

double approximate(double x, double x1, double x2, double y1, double y2)
{
    /*
     * x1 -> y1
     * x  -> y
     * x2 -> y2
     */
    if (fabs(x2 - x1) < 1e-3)
        return (y1 + y2) / 2.0;
    return y2 + (y1 - y2) * (x - x2) / (x1 - x2);
}

double getBeliefCoef(double x, double x1, double x2)
{
    // if (fabs(x2 - x1) < 1e-3)
    //     return 1.0;
    return (x2 - x) / (x2 - x1);
}

double MSE(double test[n], double given[n])
{
    double error = 0.0;
    for (int i = 0; i < (int)(n * 0.8); i++)
        error += pow(test[i] - given[i], 2.0);
    return sqrt(error / (double)(n-1)); 
}