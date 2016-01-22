#ifndef GRAHAM_SCAN_H_
#define GRAHAM_SCAN_H_

class point {
	double x, y, pAngle;
public:
	point();
	point(double, double);

	double getX()const;
	double getY()const;
	double getpAngle()const;

	void setX(double);
	void setY(double);
	void setpAngle(double);
};

point::point() :
x{0.0}, y{0.0}, pAngle{0.0} { }

point::point(double a, double b) :
x{a}, y{b}, pAngle{0.0} { }

double point::getX()const{
	return x;
}

double point::getY()const{
	return y;
}

double getpAngle()const{
	return pAngle;
}

void setX(double a){
	x = a;
}

void setY(double b){
	y = b;
}

void setpAngle(double p){
	pAngle = p;
}

#endif 