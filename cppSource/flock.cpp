#include "flock.h"

flock::flock(int n) : flock{n, 0, DEF_DIM, 0, DEF_DIM, 0, DEF_DIM} {}

flock::flock(int n, double xL, double xH, double yL, double yH, double zL, double zH) : 
	boids{n, boid()}, xMin{xL}, xMax{xH}, yMin{yL}, yMax{yH}, zMin{zL}, zMax{zH} 
	centProp{0.01}, distProp{100}, speedProp{8}, veloLim{100},
	xPad{10}, yPad{10}, zPad{10} {}

void flock::initPositions(){

}

void flock::setProps(double a, double b, double c){
	centProp = a;
	distProp = b;
	speedProp = c;
}

void flock::setVeloLimit(double v){
	veloLim = v;
}

void flock::setPadding(double x, double y, double z){
	xPad = x;
	yPad = y;
	zPad = z;
}

void flock::moveBoids(){
	for (size_t i = 0; i < boids.size(); i++){
		vec3 v1 = rule1(i);
		vec3 v2 = rule2(i);
		vec3 v3 = rule3(i);
		vec3 v4 = bound(i);

		boids[i].velo += v1;
		boids[i].velo += v2;
		boids[i].velo += v3;
		boids[i].velo += v4;
		limitVelo(i);
		boids[i].pos += boids[i].velo;
	}
}

vec3 flock::rule1(size_t b){ // move towards center
	vec3 c();
	for (size_t i = 0; i < boids.size(); i++){
		if (i == b)
			continue;
		c += boids[i].pos;	
	}
	c /= double(boids.size()-1);
	return (c - boids[b].pos)*centProp;
}
vec3 flocK::rule2(size_t b){ // keep a small distance from other boids
	vec3 c();
	for (size_t i = 0; i < boids.size(); i++){
		if (i == b)
			continue;
		double p1 = boids[b].pos.norm();
		double p2 = boids[i].pos.norm();
		if (fabs(p1-p2) < distProp)
			c -= (boids[b].pos - boids[i].pos);
	}
	return c;
}
vec3 flock::rule3(size_t b){ // try to match velocity with other biods
	vec3 c();
	for (size_t i = 0; i < boids.size(); i++){
		if (i == b)
			continue;
		c += boids[i].velo;
	}
	c /= double(boids.size()-1));
	return (c - boids[b].velo) / speedProp;
}
void flock::limitVelo(size_t b){
	vec3 c();
	if (boids[b].velo.norm() > veloLim)
		boids[b].velo *= double(veloLim / boids[b].velo.norm());
}
vec3 flock::bound(size_t b){
	vec3 c();

	if (boids[b].pos.x1 < xMin)
		c.x1 = xPad;
	else if (boids[b].pos.x1 > xMax)
		c.x1 = -xPad;
	if (boids[b].pos.x2 < yMin)
		c.x2 = yPad;
	else if (boids[b].pos.x2 > yMax)
		c.x2 = -yPad;
	if (boids[b].pos.x3 < zMin)
		c.x3 = zPad;
	else if (boids[b].pos.x3 > zMax)
		c.x3 = -zPad;

	return c;
}