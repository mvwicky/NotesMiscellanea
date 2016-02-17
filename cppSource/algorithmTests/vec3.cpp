#include "vec3.h"

vec3::vec3() : x1{0}, x2{0}, x3{0} {}

vec3::vec3(double a, double b, double c) : x1{a}, x2{b}, x3{c} {} 

vec3::vec3(const vec3 &rhs): x1{rhs.x1}, x2{rhs.x2}, x3{rhs.x3} {}
vec3 &operator=(const vec3 &rhs){
	x1 = rhs.x1;
	x2 = rhs.x2;
	x3 = rhs.x3;
	return *this;
}

double vec3::normSquared()const{
	return x1*x1 + x2*x2 + x3*x3;
}
double vec3::norm()const{
	return sqrt(normSquared());
}


vec3 &vec3::operator+=(const double rhs){
	x1 += rhs;
	x2 += rhs;
	x3 += rhs;
	return *this;
}
vec3 &vec3::operator+=(const vec3 &rhs){
	x1 += rhs.x1;
	x2 += rhs.x2;
	x3 += rhs.x3;
	return *this;
}

vec3 &vec3::operator-=(const double &rhs){
	x1 -= rhs;
	x2 -= rhs;
	x3 -= rhs;
	return *this
}
vec3 &vec3::operator-=(const vec3 &rhs){
	x1 -= rhs.x1;
	x2 -= rhs.x2;
	x3 -= rhs.x3;
	return *this;
}

vec3 &vec3::operator*=(const double rhs){
	x1 *= rhs;
	x2 *= rhs;
	x3 *= rhs;
	return *this;
}

vec3 &vec3::operator/=(double rhs){
	x1 /= rhs;
	x2 /= rhs;
	x3 /= rhs;
	return *this;
}

vec3 vec3::operator+(const double rhs)const{
	return vec3(*this) += rhs;
}
vec3 vec3::operator+(const vec3 &rhs)const{
	return vec3(*this) += rhs;
}
vec3 vec3::operator-(const double rhs)const{
	return vec3(*this) -= rhs;
}
vec3 vec3::operator-(const vec3 &rhs)const{
	return vec3(*this) -= rhs;
}
vec3 vec3::operator*(const double rhs)const{
	return vec3(*this) *= rhs;
}
vec3 vec3::operator/(const double rhs)const{
	return vec3(*this) /= rhs;
}