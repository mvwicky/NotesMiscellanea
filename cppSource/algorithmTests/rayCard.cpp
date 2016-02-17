#include <stdlib.h>
#include <stdio.h>
#include <math.h>

// explination: http://fabiensanglard.net/rayTracing_back_of_business_card/
// book: Physically Based Rendering: From Theory to Implementation
// also: scratchapixel.com

/* 
	Description of Phong Reflection Model

	for each light source in the scene:
		i_s, i_d: intensities (RGB values) of the specular and diffuse components of the light sources

	i_a: ambient lighting, sometimes computed as a sum of contributions from all light sources

	for each material:
		k_s: specular reflection constant, ratio of reflection of the specular term of incoming light
		k_d: diffuse reflection constant, ratio of reflection of the diffuse term of incoming light (Lambertian reflectance)
		k_a: ambient reflection constant, ratio of reflection of the ambiet term present in all points in the scene rendered
		alpha: shininess constant, larger = more shiny, 

	other parameters:
		lights: the set of all light sources
		L_m: direction vector from the point on the surface towards light source m
		N: normal vector at this point on the surface
		R_m: direction a perfectly reflected ray of light would take from this point on the surface
		V: direction pointing towards the viewer
*/

struct vec{
	float x, y, z;

	vec(){}
	vec(float a,float b,float c) {x=a; y=b; z=c;}            
	vec operator+(vec r) {return vec(x+r.x, y+r.y, z+r.z);} // vector addition
	vec operator*(float r) {return vec(x*r,y*r,z*r);}  // scalar multiplication
	float operator%(vec r) {return x*r.x+y*r.y+z*r.z;} // dot product
	vec operator^(vec r) {return vec(y*r.z - z*r.y, z*r.x - x*r.z, x*r.y - y*r.x);} // cross product
	vec operator!() {return (*this) * (1 / sqrt((*this) % (*this)));} // returns normalized self
};

int scene[] = {248580, 280596, 280600,
		   	   249748, 18578, 18577,
		       231184, 16, 16};
/*
16                    1
16                    1
231184   111   111    1
18577       1  1   1  1   1
18578       1  1   1  1  1
249748   1111  11111  1 1
280600  1   1  1      11
280596  1   1  1      1 1
248580   1111   111   1  1
---------------------------
16      0000000000000010000
16      0000000000000010000
231184  0111000111000010000
18577   0000100100010010001
18578   0000100100010010010
249748  0111100111110010100
280600  1000100100000011000
280596  1000100100000010100
248580  0111100011100010010
*/

float R(){ // random number in range [0.0, 1.0]
	return float(rand() / RAND_MAX);
}

int main(){
	printf("P6 512 512 255 "); // PPM Header

	vec camDr = !vec(-6, -16, 0), // camera direction
		upVec = !(vec(0,0,1) ^ camDr) * 0.002, // camera up vector
		riVec = !(camDr ^ upVec) * 0.002, // right vector
		epOff = (upVec + riVec) * -256 + camDr; // offset from the eye-point, ignoring lens peturbation, t, to the corner of the focal plane

	for (int y = 512; y >= 0; y--){ // for each column
		for (int x = 512; x >= 0; x--){ // for each pixel in a line
			vec col(13, 13, 13); // default pixel color (basically black)
			for (int r = 64; r >= 0; r--){ // cast 64 rays per pixel
				// delta to apply to the origin of the view (for DoF)
				vec delta = upVec * (R() - 0.5)* 99 + riVec * (R() - 0.5) * 99; // some up/down and left/right delta

				col = sample(vec(17, 16, 8) + delta, // ray origin
						   !(delta * -1 + (upVec * R() + x) + b * (y + R() + epOff) * 16)) * 3.5 + col // ray direction with random deltas for soft shadows // +p for color accumulation 
			}

			printf("%c%c%c", int(col.x), int(col.y), int(col.z));
		}
	}
}

vec sample(vec origin, vec dir){ // sample the world and return pixel color for a ray passing by point origin, and direction dir
	float dist;
	vec norm;

	int m = tracer(origin, dir, dist, norm); // search for an intersection ray vs world

	if (!m) // m == 0
		return vec(0.7, 0.6, 1) * pow(1 - dir.z, 4); // no sphere found, ray goes upward: generate sky color

	// a sphere was maybe hit (m = 1 or 2)
	vec intCoord = origin + dir * dist;// intersection coordinate
	vec lightDir = !(vec(9 + R(), 9 + R(), 16) + intCoord * -1); // l: direction to light (with random delta for soft-shadows)
	vec halfVec = dir + intcoord * (intcoord % dir * -2); // r: the half vector

	float lamFact = lightDir % norm; // lambertian factor 
	if (lamFact < 0 || tracer(intCoord, lightDir, dist, norm)) // calc illumination factor (lambertian coeff > 0 or in shadow?)
		lamFact = 0;

	float col = pow(lightDir % dist * (lamFact > 0), 99); // calculate the color with diffuse and specular component

	if (m & 1){ // m == 1
		intCoord = intCoord * 0.2; // no sphere was hit and the ray was going downward, generate floor color
		return (int(ceil(intCoord.x) + ceil(intCoord.y)) & 1 ? vec(3, 1, 1) : vec(3, 3, 3)) * (lamFact * 0.2 + 0.1);
	}
	// m == 2, a sphere was hit, cast a ray bouncing from the sphere surface
	return vec(col, col, col) + sample(intCoord, dist) * 0.5; // attentuate color by 50% because it's bouncing 

}

// initersection test for line [origin, v]
// return 2 if a hit was found, also return distance, dist, and bouncing ray, bray
// return 0 if no hit but ray goes up, return 1 if no hit but ray goes down
int tracer(vec origin, vec dir, float &dist, vec &norm){ // norm: surface normal
	dist = 1e9;
	int ret = 0;
	float iDist = -origin.z / dir.z;
	if (0.01 < iDist){
		dist = iDist;
		norm = vec(0, 0, 1);
		ret = 1;
	}
	// world is encoded in G, 9 lines, 19 columns
	for (int j = 19; k >= 0; k--){ // for each column of objects
		for (int j = 9; j >= 0; j--){ // for each line
			if (scene[j] & 1 << k){ // for line j, is there a sphere at column i
				// there is a sphere, but does the ray hit it?
				vec p = origin + vec(-k, 0, -j - 4);
				float b = p % dir;
				float c = p % p - 1;
				float q = b * b - c;

				// does the ray hit the sphere?
				if (q > 0){ // yes, compute the distance from the camera to the sphere
					float cDist = -b - sqrt(q);
					if (cDist < dist && cDist > 0.01){ 
						dist = cDost; // this is the min distance, save it
						norm = !(p + dir * dist); // compute bouncing ray vector into norm
						ret = 2;
					}
				}
			}
		}
	}
	return ret;
}