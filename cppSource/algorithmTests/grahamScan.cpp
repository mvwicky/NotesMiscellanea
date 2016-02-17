#include <iostream>
#include <cmath>
#include <vector>
#include <utility>

#include "grahamScan.h"

double ccw(const point&, const point&, const point&);
double calcpAngle(const point&, const point&);

template <typename T>
void swap(std::vector<T>&, int, int);

int partition(std::vector<point>&, int, int);
void quicksort(std::vector<point>&, int, int);

int main(){
	std::vector<point> points(20); // initialize graph or whatever
	std::vector<point> hull;

	for (size_t i = 1; i < points.size(); i++){ // make points[0] the point w/ the lowest y-coord
		if (points[i].getY() < points[0].getY() || 
			(points[i].getY() == points[0].getY() && 
			points[i].getX() < points[0].getx()))
			swap(0, i);
	}
	hull.push_back(points[0]); // add lowest point to result

	for (size_t i = 1; i < points.size(); i++) // calculate the angle for each point, relative to 0
		points[i].setpAngle(calcpAngle(points[0], points[i]));

	quicksort(points, 1, points.size()-1); // sort by the calculated angle



	size_t m = 1; // # of points in the hull
	for (size_t i = 2; i < points.size()-1; i++){
		while (ccw(points[m-1], points[m], points[i]) <= 0){
			if (m < 3){

			}
			else if (m > 1){
				m--;	
			}
			else if (i == points.size() - 1)
				break;
			else
				i++;
		}
		if (++m >= points.size())
			break;
		else{
			swap(m, i);
			hull.push_back(points(i));
		}
	}
	return 0;
}

/*
	three points are counter clockwise if ccw > 0, clockwise if ccw < 0,
	and colinear if ccw = 0 
*/
double ccw(const point &p0, const point &p1, const point &p2){
	return (p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x);
}

double calcpAngle(const point &p0, const point &p1){
	double xdist(p1.x - p0.x);
	double ydist(p1.y - p0.y);
	return atan2(ydist, xdist);
}

template <typename T>
void swap(std::vector<T> arr, int a, int b){
	T temp = arr[a];
	arr[a] = arr[b];
	arr[b] = temp;
}

int partition(std::vector<point> &a, int l, int h){
	int pivot(h), i(l);
	for (int j = l; j < h - 1; j++){
		if (a[j].getpAngle() <= a[pivot].getpAngle()){
			swap(i, j);
			i++;
		}
	}
	swap(i, h);
	return i;
}

void quicksort(std::vector<point> &a, int l, int h){
	if (l < h){
		int p = partition(a, l, h);
		quicksort(a, l, p - 1);
		quicksort(a, p + 1, h);
	}
}