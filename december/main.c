#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#define MAX_TST 5
#define FXPOINT 0.75
#define SCALE   1
const char* fName = "./src/T.csv";
const char* gName = "./src/D.csv";
const char* tfName = "./src/_T.csv";
const char* tgName = "./src/_D.csv";
const char* ioName = "io.csv";
const int m = 21, n = 81;

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

double better_approximate(double x, double x1, double x2, double y1, double y2)
{
    if (fabs(x2 - x1) < 1e-3)
        return (y1 + y2) / 2.0;
    
    double _x  = log(x),
           _x1 = log(x1), _y1 = log(y1),
           _x2 = log(x2), _y2 = log(y2);

    return exp(approximate(_x, _x1, _x2, _y1, _y2));
    
    // double f = (log(x) - log(x1)) / (log(x2) - log(x1));
    // return pow(y1, 1.0-f) * pow(y2, f);
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
    for (int i = 0; i < (int)(n * FXPOINT); i++)
        error += pow(test[i] - given[i], 2.0);
    return sqrt(error / (double)(n-1)); 
}

int main(int argc, char **argv)
{
    FILE *fs = fopen(fName, "r"),
         *gs = fopen(gName, "r");;
    if (!fs || !gs)
        return -1;

    rewind(fs);
    rewind(gs);

    double input[m][n], output[m][n];

    for (int i = 0; i < m; i++)
    {
        for (int j = 0; j < n; j++)
        {
            fscanf(fs, "%lf,", &input[i][j]);
            fscanf(gs, "%lf,", &output[i][j]);
            // fix IO
            output[i][j] *= SCALE;
        }
    }
    
    fclose(fs);
    fclose(gs);

    fs = fopen(tfName, "r");
    gs = fopen(tgName, "r");
    if (!fs || !gs)
        return -1;

    rewind(fs);
    rewind(gs);
    
    double test_input[MAX_TST][n], test_output[MAX_TST][n];

    for (int i = 0; i < MAX_TST; i++)
    {
        for (int j = 0; j < n; j++)
        {
            fscanf(fs, "%lf,", &test_input[i][j]);
            fscanf(gs, "%lf,", &test_output[i][j]);
            // fix tests
            test_output[i][j] *= SCALE;
        }
    }
    
    fclose(fs);
    fclose(gs);

    double result[MAX_TST][n];
    
    int debug = atoi(argv[1]), p = 0, q = 0;
    if (debug)
    {
        p = atoi(argv[2]);
        q = atoi(argv[3]);
    }

    int imax = m-1;

    // Idea: Sugeno algorithm in fuzzy logic    
    for (int k = 0; k < MAX_TST; k++)
    {
        for (int j = 0; j < n; j++)
        {
            double value = test_input[k][j];
            double MY = 0.0, MX = 0.0;
            
            for (int i = 0; i < imax; i++)
            {
                double b_coef = getBeliefCoef(value, input[i][j], input[imax][j]);
                //double approximatedValue = approximate(value, input[i][j], input[imax][j], output[i][j], output[imax][j]);
                double approximatedValue = better_approximate(value, input[i][j], input[imax][j], output[i][j], output[imax][j]);
                MX += b_coef;
                MY += b_coef * approximatedValue;

                if (debug && k == p && j == q)
                {
                    printf("Step %d: In(%10.3f,%10.3f)\tOut(%10.3f, %10.3f)\n", i, input[i][j], input[imax][j], output[i][j], output[imax][j]);
                    printf("        x=%0.3f\ty=%.4f\tb=%.4f\n\n", value, approximatedValue, b_coef);
                }
            }

            result[k][j] = MY / MX;
        }
    }
    // for (int k = 0; k < n; k++)
    // {
    //     printf("Result: %.3f : %.3f\n", result[k], test_output[k]);
    // }
    if (debug)
        printf("Result: %.3f\tNeed: %.3f\n", result[p][q], test_output[p][q]);

    int pmin;
    double mse[MAX_TST], min, max;
    for (int i = 0; i < MAX_TST; i++)
    {
        mse[i] = MSE(result[i], test_output[i]);
        if (i == 0)
        {
            pmin = 0;
            min = max = mse[i];
        }
        else
        {
            if (mse[i] < min)
            {
                pmin = i;
                min = mse[i];
            }
            if (mse[i] > max)
                max = mse[i];
        }
    }

    if (debug)
        printf("pMSE: %.5f\n", mse[p]);

    FILE *io = fopen(ioName, "w");
    if (!io)
        return -1;

    fprintf(io, "Approximate,Exact,RelError");
    printf("Result:\n");
    for (int i = 0; i < (int)(n * FXPOINT); i++)
    {
        double  absError = fabs(result[pmin][i] - test_output[pmin][i]),
                relError = absError / fabs(test_output[pmin][i]);

        fprintf(io, "\n%.5f,%.5f,%E", result[pmin][i], test_output[pmin][i], relError);
        printf("approx=%10.5f\texact=%10.5f\tabsError=%.5f\trelError=%.5f\n", \
                result[pmin][i], test_output[pmin][i], absError, relError);
    }
    printf("MSE: best=%.5f, worth=%.5f\n", min, max);
    
    fclose(io);
    return 0;
}