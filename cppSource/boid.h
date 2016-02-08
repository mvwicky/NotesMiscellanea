#ifndef _BOID_H_
#define _BOID_H_

#include "vec3.h"

class boid {
public:
	vec3 pos, velo;

	boid() : boid{0, 0, 0} {} 
	boid(double a, double b, double c) : x{a}, y{b}, z{c} {}
};

#endif