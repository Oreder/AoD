#include "util.h"

int main(int argc, char **argv)
{
    FILE *fs = fopen("../src/T.csv", "r"),
         *gs = fopen("../src/D.csv", "r");;
    if (!fs || !gs)
        return -1;

    rewind(fs);
    rewind(gs);

    double input[m][n], output[m][n], head[m];

    for (int i = 0; i < m; i++)
    {
        for (int j = 0; j < n; j++)
        {
            fscanf(fs, "%lf,", &input[i][j]);
            fscanf(gs, "%lf,", &output[i][j]);
        }
    }
    
    fclose(fs);
    fclose(gs);

    fs = fopen("../src/_T.csv", "r");
    gs = fopen("../src/_D.csv", "r");
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
        }
    }
    
    fclose(fs);
    fclose(gs);

    double result[MAX_TST][n];
    
    int debug = atoi(argv[1]), p, q;
    if (debug)
    {
        p = atoi(argv[2]);
        q = atoi(argv[3]);
    }

    // Idea: Sugeno algorithm in fuzzy logic + kNN
    for (int k = 0; k < MAX_TST; k++)
    {
        // Let find kNN
        for (int i = 0; i < m; i++)
            head[i] = input[i][0];      // 0 - fixed position

        int begin = getChosenIndexBegin(test_input[k][0], head);
        
        // set up base line
        int base = (begin == 0)? (begin + chosen) : (begin - 1);

        for (int j = 0; j < n; j++)
        {
            double value = test_input[k][j];
            double MY = 0.0, MX = 0.0;
            
            // for (int i = 0; i < m-1; i++)
            for (int j = 0; j < chosen && begin + j + 1 < m; j++)
            {
                int i = begin + j;
                double b_coef = getBeliefCoef(value, input[i][j], input[base][j]);
                double approximatedValue = approximate(value, input[i][j], input[base][j], output[i][j], output[base][j]);
                MX += b_coef;
                MY += b_coef * approximatedValue;

                if (debug && k == p && j == q)
                {
                    printf("Step %d: In(%10.3f,%10.3f)\tOut(%10.3f, %10.3f)\n", i, input[i][j], input[base][j], output[i][j], output[base][j]);
                    printf("        x=%0.3f\ty=%.4f\tb=%.4f\n\n", value, approximatedValue, b_coef);
                }
            }

            result[k][j] = MY / MX;
        }
    }

    fs = fopen("../src/BINH.csv", "w");
    for (int i = 0; i < MAX_TST; i++)
    {
        for (int j = 0; j < n - 1; j++)
            fprintf(fs, "%.5f,", result[i][j]);
        fprintf(fs, "%.5f\n", result[i][n-1]);

        for (int j = 0; j < n - 1; j++)
            fprintf(fs, "%.5f,", test_output[i][j]);
        fprintf(fs, "%.5f\n\n", test_output[i][n-1]);
    }
    fclose(fs);
    
    if (debug)
        printf("Result: %.3f\tNeed: %.3f\n", result[p][q], test_output[p][q]);
    
    double mse[MAX_TST], min, max;
    for (int i = 0; i < MAX_TST; i++)
    {
        mse[i] = MSE(result[i], test_output[i]);
        if (i == 0)
        {
            min = max = mse[i];
        }
        else
        {
            if (mse[i] < min)
                min = mse[i];
            if (mse[i] > max)
                max = mse[i];
        }
    }

    if (debug)
        printf("pMSE: %.5f\n", mse[p]);

    printf("MSE: best=%.5f, worth=%.5f\n", min, max);

    return 0;
}