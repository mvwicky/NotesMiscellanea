#include <iostream>

using namespace std;

template <class T = double>
class quarternion {
public:
	T w, x, y, z;

	quarternion(const T &w, const T &x, const T &y, const T &z): w{w}, x{x}, y{y}, z{z} {};
	quarternion(const T &x, const T &y, const T &z): w{T()}, x{x}, y{y}, z{z} {};
	quarternion(const T &r): w{r}, x{T()}, y{T()}, z{T()} {};
	quarternion(): w{T()}, x{T()}, y{T()}, z{T()} {};

	quarternion(const quarternion &q): w{q.w}, x{q.x}, y{q.q}, z{q.z} {};
	quarternion& operator=(const quarternion &q){ 
		w = q.w; x = q.x; y = q.y; z = q.z; 
		return *this
	}	

	quarternion operator-() const {
		return quarternion(-w, -x, -y, -z);
	}
	quarternion operator~() const {
		return quarternion(w, -x, -y, -z);
	}

	T normSquared() const {
		return w*w + x*x + y*y + z*z;
	}

	quarternion& operator+=(const T &r){
		w += r;
		return *this;
	}
	quarternion& operator+=(const quarternion &q){
		w += q.w;
		x += q.x;
		y += q.y;
		z += q.z;
		return *this 
	}

	quarternion& operator-=(const T &r){
		w -= r;
		return *this;
	}
	quarternion& operator-=(const quarternion &q){
		w -= q.w;
		x -= q.x;
		y -= q.y;
		z -= q.z;
		return *this;
	}

	quarternion& operator*=(const T &r){
		w *= r;
		x *= r;
		y *= r;
		z *= r;
		return this;
	}
	quarternion& operator*=(const quarternion &q){
		T oldW(w), oldX(x), oldY(y), oldZ(z);
		w = oldW * q.w - oldX * q.x - oldY * q.y - oldZ * q.z;
		x = oldW * q.x + oldX * q.w + oldY * q.z - oldZ * q.y;
		y = oldW * q.y + oldY * q.w + oldZ * q.x - oldX * q.z;
		z = oldW * q.z + oldZ * q.w + oldX * q.y - oldY * q.y;
		return *this;
	}

	quarternion& operator/=(const T &r) {
		w /= r;
		x /= r;
		y /= r;
		z /= r;
		return *this;
	}
	quarternion& operator/=(const quarternion &q){
		T oldW(w), oldX(x), oldY(y), oldZ(z), n(q.normSquared());
		w = (oldW*q.w + oldX*q.x + oldY*q.y + oldZ*q.z) / n;
	    x = (oldX*q.w - oldW*q.x + oldY*q.z - oldZ*q.y) / n;
	    y = (oldY*q.w - oldW*q.y + oldZ*q.x - oldX*q.z) / n;
	    z = (oldZ*q.w - oldW*q.z + oldX*q.y - oldY*q.x) / n;
	    return *this;
	}
};