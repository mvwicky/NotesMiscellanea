import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

def mph_to_mps(mph):
	return mph * (1609.34 / 60**2)

def deg_to_rad(deg):
	return deg * (np.pi / 180)

def calc_rho(h, T=None):
	p_o = 101325 # Pa
	L = 0.0065 # K/m
	T_o = 288.15 # K
	R = 8.31447 # J/mol*K
	M = 0.0289644 # kg/mol
	g = 9.80665 # m/s^2
	if (T == None):
		T = T_o - L*h # temp at altitude h
	p = p_o * (1 - (L * h) / T_o)**((g*M)/(R*L)) # absolute pressure at altitude h
	rho = (p * M) / (R * T)
	return rho

print(calc_rho(0))

def rho(h, T=None):
	if (T == None):
		T = 288.15 - 0.0065 * h 
	p = 101325 * (1 - (0.0065 * h) / 288.15)**((9.80665 * 0.0289644)/(8.31447 * 0.0065))
	return (p * 0.0289644) / (8.31447 * T)


# TODO
#
# find out how to stop drawing of line at 'ground' 
# add drag due to air
#	need to add attributes to battedBall class
#		m -> mass: 0.145 kg
#		A -> frontal area: pi*r^2
#			r = 73 mm (73 * 10^-3 m)
#		C_D -> coefficient of drag: 0.3 (dimensionless)
#			ref for number: www.grc.nasa.gov/www/k-12/airplane/balldrag.html
#		rho -> dependent on:
#			p_o -> sea level std. atmospheric pressure: 101.325 * 10^3 Pa
#			L -> temperature lapse rate: 0.0065 K/m
#			T_o -> sea level std. temperature: 288.15 K
#			R -> ideal gas constant: 8.31447 J/mol*K
#			M -> molar mass of air: 0.0289644 kg/mol
#			g -> acceleration due to gravity: 9.80665 m/s^2
#			h -> altitude in meters (input)
#			p -> absolute pressure in pascals: p_o(1 - Lh/T_o)^(gM/RL)
#			T -> absolute temperature: T_o - Lh
#			rho = pM/RT
#		k -> drag factor:
#			k = 0.5 * rho * A * C_D
# 		v_x -> horizontal velocity
#			v_x0 -> initial velocity in the x direction: v_tot*cos(phi)*sin(90-theta)
#			v_x(t) = 1 / ((1 / v_x0) + (kt/m)) = (v_x0^-1 + (kt/m))^-2
#			v_x and v_y will be equal, but with different exit vectors 
#				v_y0 -> initial velo in y: v_tot*sin(phi)*cos(90-theta)
#		s_x, s_y -> horizontal distance traveld
#		vertical velocity and distance
#			has two parts
#			upward:
#				
#			downward:



class battedBall(object):
	"""v_tot in meters per second
	   theta and phi in radians
	   g is a constant"""
	def __init__(self, v_tot, theta, phi, g=-9.08665, freq=30):
		self.v_tot = v_tot
		self.theta = theta # angle from horzontal (up = +, down = -)
		self.phi = phi # azimuthal angle (0 = 1st base, 90 or pi/2 = 3rd base)
		self.g = g # gravitational acceleration
		self.freq = freq # samples per second
		self.theta_p = deg_to_rad(90) - self.theta
		self.v_vec = [self.v_tot * np.cos(self.phi) * np.sin(self.theta_p), # x = r * cos(phi) * sin(90 - theta)
					  self.v_tot * np.sin(self.phi) * np.cos(self.theta_p), # y = r * sin(phi) * cos(90 - theta)
					  self.v_tot * np.cos(self.theta_p)]                    # z = r * cos(90 - theta)
		self.t_tot = (-2 * self.v_vec[2]) / self.g
		self.z_max = (self.v_vec[2]**2) / (-2 *g)

		self.n_samps = np.ceil(self.t_tot) * self.freq
		self.samp_vec = np.linspace(0, np.ceil(self.t_tot), self.n_samps)

		self.x_vec = self.v_vec[0] * self.samp_vec 
		self.y_vec = self.v_vec[1] * self.samp_vec
		self.z_vec = 1 + self.v_vec[2]*self.samp_vec + 0.5 * self.g * self.samp_vec**2
	def printAttr(self):
		print("|V| =", self.v_tot)
		print("theta, phi =", self.theta, self.phi)
		print("(vx, vy, vz) =", self.v_vec[0], self.v_vec[1], self.v_vec[2])
		print("Number of Samples:", self.n_samps)


# theta: angle from horizonal
# phi: angle from straight away center
#	phi(CF) = pi / 4
#	1st base line: 0
#	3rd base line: pi / 2
# if phi < 0 or phi > (pi / 2) -> foul ball

# mass: 0.145 kg
# r

v_tot = mph_to_mps(110)
theta = deg_to_rad(30)
theta_p = deg_to_rad(90) - theta # 90 - theta
phi = deg_to_rad(45)

bb1 = battedBall(v_tot, theta, phi)
bb2 = battedBall(mph_to_mps(80), deg_to_rad(20), deg_to_rad(90))
bb1.printAttr()
 
#b_vec = [battedBall(mph_to_mps(100),deg_to_rad((i+10)/2), deg_to_rad(2*i)) for i in range(45)]


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(bb1.x_vec, bb1.y_vec, bb1.z_vec)
ax.plot(bb2.x_vec, bb2.y_vec, bb2.z_vec)

#for i in b_vec:
#	ax.plot(i.x_vec, i.y_vec, i.z_vec)

ax.autoscale()
ax.set_zbound(0, 50)
plt.show()