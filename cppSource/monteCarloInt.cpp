#include "monteCarloInt.h"

integrator::integrator(int N, std::vector<double> &c, double xL, double xH) : 
	nSamps{N}, coeffs{c}, xMin{xL}, xMax{xH}, yMin{0} {
	
}