#include "util.h"

double approximate(double x, double x1, double x2, double y1, double y2)
{
    return y2 - (y2 - y1) * getBeliefCoef(x, x1, x2);
}

double getBeliefCoef(double x, double x1, double x2)
{
    return (x2 - x) / (x2 - x1);
}

double MSE(double test[n], double given[n])
{
    double error = 0.0;
    for (int i = 0; i < n; i++)
        error += pow(test[i] - given[i], 2.0);
    return sqrt(error / (double)(n-1)); 
}