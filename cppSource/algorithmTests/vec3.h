#ifndef _VEC3_H_
#define _VEC3_H_

#include <cmath>

class vec3 {
public:
	double x1, x2, x3;

	vec3(); 
	vec3(double, double, double); 

	vec3(const vec3&);
	vec3 &operator=(const vec3&);

	double normSquared()const;
	double norm()const;


	vec3 &operator+=(const double&);
	vec3 &operator+=(const vec3&);

	vec3 &operator-=(const double&);
	vec3 &operator-=(const vec3&);

	vec3 &operator*=(const double&);

	vec3 &operator/=(cosnt double&);

	vec3 operator+(const double&)const;
	vec3 operator+(const vec3&)const;
	vec3 operator-(const double&)const;
	vec3 operator-(const vec3&)const;
	vec3 operator*(const double&)const;
	vec3 operator/(const double&)const;
};

#endif 