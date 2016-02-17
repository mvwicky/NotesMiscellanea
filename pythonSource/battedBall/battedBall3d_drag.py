import sys 

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from util import *

# theta: angle from horizonal
# phi: angle from straight away center
#	phi(CF) = pi / 4
#	1st base line: 0
#	3rd base line: pi / 2
# if phi < 0 or phi > (pi / 2) -> foul ball

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
#			v_x and v_y will be equal, but with different exit angles
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
	def __init__(self, v_tot, theta, phi, alt, T=None, g=9.08665, freq=30):
		self.v_tot = v_tot
		self.theta = theta # angle from horzontal (up = +, down = -)
		self.phi = phi # azimuthal angle (0 = 1st base, 90 or pi/2 = 3rd base)
		self.alt = alt # altitude in meters
		self.g = g # gravitational acceleration
		self.freq = freq # samples per second

		theta_p = np.deg2rad(90) - self.theta # complement of theta 
		self.v_i = [self.v_tot * np.cos(self.phi) * np.sin(theta_p), # x = r * cos(phi) * sin(90 - theta)
					self.v_tot * np.sin(self.phi) * np.sin(theta_p), # y = r * sin(phi) * cos(90 - theta)
					self.v_tot * np.cos(theta_p)]                    # z = r * cos(90 - theta)

		# constants
		c_p_o = 101325 # Pa
		c_L = 0.0065 # K/m
		c_T_o = 288.15 # K
		c_R = 8.31447 # J/mol*K
		c_M = 0.0289644 # kg/mol
		
		if (T == None):
			self.T = c_T_o - c_L*self.alt # calc temp at altitude alt
		else:
			self.T = T # get temp from input

		p = c_p_o * (1 - (c_L * self.alt) / c_T_o)**((self.g*c_M)/(c_R*c_L)) # absolute pressure at altitude h
		
		self.rho = (p * c_M) / (c_R * self.T) # air density at altitude alt

		self.mass = 0.145 # kg
		F_A = np.pi * 0.0073**2 # frontal area 
		C_D = 0.3 # drag coefficient (of sphere)
		self.k = 0.5 * self.rho * F_A * C_D # drag factor

		self.z_max = -1 * (self.mass / self.k) * np.log(np.cos(np.arctan(np.sqrt(self.k / (self.mass * self.g)) * self.v_i[2]))) # apex of flight

		self.t_a = np.sqrt(self.mass / (self.g * self.k)) * np.arctan(np.sqrt(self.k / (self.mass * self.g)) * self.v_i[2]) # ascent time
		self.t_d = np.sqrt(self.mass / (self.g * self.k)) * np.arccosh(np.sqrt(1 + ((self.k * self.v_i[2]**2) / (self.g * self.mass)))) # descent time 

		self.t_tot = self.t_a + self.t_d # total time


		self.n_samps = np.ceil(self.t_tot) * self.freq
		self.samp_vec = np.linspace(0, self.t_tot, self.n_samps)

		self.x_vec = [self.s_t('x', i) for i in self.samp_vec]
		self.y_vec = [self.s_t('y', i) for i in self.samp_vec]
		self.z_vec = [self.s_t('z', i) for i in self.samp_vec]


	def printAttr(self):
		print("|V| =", self.v_tot)
		print("theta, phi =", self.theta, self.phi)
		print("(vx, vy, vz) =", self.v_i)
		print(np.sqrt(self.v_i[0]**2 + self.v_i[1]**2 + self.v_i[2]**2))
		print("Number of Samples:", self.n_samps)
		print("Ascent Time: {} Descent Time: {}".format(self.t_a, self.t_d))
		print("Total Time:", self.t_tot)
		print("Max Height:", self.z_max)

	def s_t(self, d, t): # calculate distance at time, t , for direction, d
		if d == 'x': # x direction
			return (self.mass / self.k) * np.log((self.k * t * self.v_i[0] + self.mass) / self.mass)
		elif d == 'y': # y direction, same as x
			return (self.mass / self.k) * np.log((self.k * t * self.v_i[1] + self.mass) / self.mass)
		elif d == 'z':
			if t < self.t_a: # ascending
				c = -(self.mass / self.k) * np.log(np.cos(np.arctan(np.sqrt(self.k / (self.mass * self.g)) * self.v_i[2])))
				return (self.mass / self.k) * np.log(np.cos(np.sqrt((self.g * self.k) * self.mass) * t - np.arctan(np.sqrt(self.k / (self.mass * self.g)) * self.v_i[2]))) + c
			elif t > self.t_a: # descending
				t -= self.t_a
				return self.z_max - (self.mass / self.k) * np.log(np.cosh(np.sqrt((self.g * self.k) / self.mass) * t))
			elif t == self.t_a:
				return self.z_max
			elif t > self.t_tot:
				print("Time is too large")
				sys.exit(-1)
		else:
			print("Invalid Direction")
			sys.exit(-1)



v = mph_to_mps(110)
theta = np.deg2rad(20)
phi = np.deg2rad(30)

bb1 = battedBall(v, theta, phi, 0)
bb1.printAttr()

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot(bb1.x_vec, bb1.y_vec, bb1.z_vec)

ax.autoscale()

plt.show()