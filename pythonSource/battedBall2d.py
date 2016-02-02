import numpy as np
import matplotlib.pyplot as plt 

def mph_to_mps(mph):
	return mph * (1609.34 / 60**2)

def deg_to_rad(deg):
	return deg * (np.pi / 180)


# constants
g = -9.08665 # m / s**2
freq = 60 # hz
dt = 1 / freq # s

# inputs
v_tot = mph_to_mps(85)
theta = deg_to_rad(15)

# velocity as a vector
v_vec = [v_tot * np.cos(theta) , v_tot * np.sin(theta)]

t = (-2 * v_vec[1]) / g
t_c = np.ceil(t)
z_max = (v_vec[1]**2) / (-2 * g)

print(z_max)

samps = t_c * freq
nn = np.linspace(0, t_c, t_c*freq)

x = v_vec[0] * nn 
z = 1 + v_vec[1]*nn + 0.5 * g * nn**2

m = x[len(x)-1]

plt.plot(x, z)
plt.axis([0, m, 0, m])
plt.show()