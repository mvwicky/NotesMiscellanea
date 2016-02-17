#ifndef _FLOCK_H_
#define _FLOCK_H_

#include <vector>

#include "vec3.h"
#include "boid.h"

class flock {
public:
	std::vector<boid> boids; 
	double xMin, xMax, yMin, yMax, zMin, zMax;
	double centProp, distProp, speedProp, veloLim;
	double xPad, yPad, zPad;

	flock();
	flock(int);
	flock(int, double, double, double, double, double, double);

	void initPositions();

	void setProps(double, double, double);

	void setVeloLimit(double);

	void setPadding(double, double, double);

	void moveBoids();

	vec3 rule1(size_t);
	vec3 rule2(size_t);
	vec3 rule3(size_t);
	void limitVelo(size_t);
	vec3 bound(size_t);

};

#endif 