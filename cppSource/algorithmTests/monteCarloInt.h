#ifndef _MONTECARLO_H_
#define _MONTECARLO_H_

#include <vector>
#include <cstdlib>
#include <cmath>

class integrator{
private:
	int nSamps;
	std::vector<double> coeffs;
	double xMin, xMax, yMin, yMax;
public:
	integrator(int, const std::vector<double>&, const double, const double);

	

};

#endif