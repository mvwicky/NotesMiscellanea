#include <iostream>
#include <iomanip>
#include <cmath>
#include <cstdlib>
#include <ctime>

#define PI 3.14159265359
#define RAND_IN_RANGE(x, y) (x + double(rand() / (double(RAND_MAX) / (y - x))))

using namespace std;

double randInRange(double, double);
double mcOpt1(int n); // optimization problem: Z = (e^{x1} + x2)^2 + 3(1 - x3)^2

int main() {
    srand(time(NULL));
    
    int nSamps(100000), hit(0);
    
    for (int i = 0; i < nSamps; i++){
        double x = (double(rand()) / double(RAND_MAX)) * PI;
        double y = double(rand()) / double(RAND_MAX);
        
        if (y <= sin(x))
            hit++;
    }
    double a = PI * double(hit) / double(nSamps);
    cout << a << endl;
}

double randInRange(double min, double max){
    return min + double(rand()) / (double(RAND_MAX) / (max - min));
}

double mcOpt1(int n){
    int hit(0);
    double x1(0), x2(0), x3(0), zmax(0);
    for (int i = 0; i < n; n++){
        double r1 = randInRange(0, 1);
        double r2 = randInRange(0, 2);
        double r3 = randInRange(2, 3);
        double z = pow((exp(r1) + r1), 2) + 3 * pow((1 - r3), 2);
        if (z > zmax){
            x1 = r1;
            x2 = r2;
            x3 = r3;
            zmax = z;
        }
    } 
    cout << "x1: " << x1 << endl;
    cout << "x2: " << x2 << endl;
    cout << "x3: " << x3 << endl;
    return 0;
}


double monteCarloInt(int nSamps, int nTerms, double *coeffs, double xMin, double xMax){ // use monte-carlo method to integrate a function
    int hit(0);
    double yMin(0), yMax(0);

    for (int i = 0; i < nTerms; i++)
        yMax += pow(xMax, i) * coeffs[i];

    double area(xMax * yMax);
    for (int i = 0; i < nSamps; i++){
        double x = randInRange(xMin, xMax);
        double y = randInRange(yMin, yMax);
        double res(0);
        for (int j = 0; j < nTerms; j++)
            res += pow(x, j) * coeffs[j];
        if (y <= res)
            hit++;
    }
    return (double(hit)/double(nSamps)) * area;
}