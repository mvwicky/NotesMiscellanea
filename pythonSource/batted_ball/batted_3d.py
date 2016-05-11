import sys

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


# constants
METERS_PER_MILE = 1609.34
STD_PRESSURE = 101325  # Pa
LAPSE_RATE = 0.0065  # K/m
STD_TEMP = 288.15  # K
GAS_CONSTANT = 8.31447  # J/mol*K
MOLAR_MASS = 0.0289644  # kg/mol
DRAG_COEFF = 0.3  # unitless
MASS = 0.143  # kg
RADIUS = 0.0074  # meters


def mph_to_mps(mph):
    return mph * (METERS_PER_MILE / 60**2)


class battedBall(object):
    """v_tot in meters per second
       theta and phi in radians
       g is a constant"""
    def __init__(self, v_tot, theta, phi, alt, T=None, g=9.08665, freq=30):
        self.v_tot = v_tot  # total velocity vector
        self.theta = theta  # angle from horzontal (up = +, down = -)
        self.phi = phi  # azimuthal angle (0 = 1st base, 90 or pi/2 = 3rd base)
        self.alt = alt  # altitude in meters
        self.g = g  # gravitational acceleration
        self.freq = freq  # samples per second

        # complement of theta
        theta_p = (np.pi / 2) - self.theta

        # calculate initial velocities per direction
        # x = r * cos(phi) * sin(90 - theta)
        # y = r * sin(phi) * cos(90 - theta)
        # z = r * cos(90 - theta)
        self.v_i = [self.v_tot * np.cos(self.phi) * np.sin(theta_p),
                    self.v_tot * np.sin(self.phi) * np.sin(theta_p),
                    self.v_tot * np.cos(theta_p)]

        self.mass = MASS

        # calc temp at altitude alt, if not given
        if not T:
            self.T = STD_TEMP - LAPSE_RATE * self.alt
        else:
            self.T = T

        # absolute pressure at altitude h
        p = STD_PRESSURE * (1 - (LAPSE_RATE * self.alt) / STD_TEMP) ** \
            ((self.g * MOLAR_MASS) / (GAS_CONSTANT * LAPSE_RATE))

        # air density at altitude alt
        self.rho = (p * MOLAR_MASS) / (GAS_CONSTANT * self.T)

        frontal_area = np.pi * RADIUS**2  # frontal area

        # calculate drag factor
        self.drag_factor = 0.5 * self.rho * frontal_area * DRAG_COEFF

        # calculate apex of flight
        self.z_max = -1 * (self.mass / self.drag_factor) * \
            np.log(np.cos(np.arctan(np.sqrt(self.drag_factor /
                                    (self.mass * self.g)) * self.v_i[2])))

        # calculate ascent time
        self.ascent_time = (np.sqrt(self.mass / (self.g * self.drag_factor)) *
                            np.arctan(np.sqrt(self.drag_factor /
                                      (self.mass * self.g)) * self.v_i[2]))

        # calculate descent time
        self.descent_time = (np.sqrt(self.mass / (self.g * self.drag_factor)) *
                             np.arccosh(np.sqrt(1 + ((self.drag_factor *
                                                      self.v_i[2]**2) /
                                                     (self.g * self.mass)))))

        self.t_tot = self.ascent_time + self.descent_time  # total time

        self.n_samps = np.ceil(self.t_tot) * self.freq
        self.samp_vec = np.linspace(0, self.t_tot, self.n_samps)

        self.x_vec = [self.dist('x', i) for i in self.samp_vec]
        self.y_vec = [self.dist('y', i) for i in self.samp_vec]
        self.z_vec = [self.dist('z', i) for i in self.samp_vec]

    def printAttr(self):
        print('|V| = {}'.format(self.v_tot))
        print('theta = {}'.format(self.theta))
        print('phi = {}'.format(self.phi))
        print('(vx, vy, vz) = {}'.format(self.v_i))
        print('Number of Samples:', self.n_samps)
        print('Ascent Time: {}\nDescent Time: {}'
              .format(self.ascent_time, self.descent_time))
        print('Total Time:', self.t_tot)
        print('Max Height:', self.z_max)

    def dist(self, direction, t):
        """ calculate distance at time, t, for the given direction """
        if direction is 'x':  # x direction
            return ((self.mass / self.drag_factor) *
                    np.log((self.drag_factor * t *
                            self.v_i[0] + self.mass) / self.mass))
        elif direction is 'y':  # y direction, same as x
            return ((self.mass / self.drag_factor) *
                    np.log((self.drag_factor * t *
                            self.v_i[1] + self.mass) / self.mass))
        elif direction is 'z':
            return self.dist_z(t)
        else:
            print("Invalid Direction")
            sys.exit(-1)

    def dist_z(self, t):
        if t < self.ascent_time:  # ascending
            c = (-(self.mass / self.drag_factor) *
                 np.log(np.cos(np.arctan(np.sqrt(self.drag_factor /
                        (self.mass * self.g)) * self.v_i[2]))))
            return ((self.mass / self.drag_factor) * np.log(np.cos(
                    np.sqrt((self.g * self.drag_factor) / self.mass) * t -
                    np.arctan(np.sqrt(self.drag_factor /
                              (self.mass * self.g)) * self.v_i[2]))) + c)
        elif t > self.ascent_time:  # descending
            return (self.z_max - (self.mass / self.drag_factor) *
                    np.log(np.cosh(np.sqrt((self.g * self.drag_factor) /
                           self.mass) * (t - self.ascent_time))))
        elif t == self.ascent_time:
            return self.z_max

        elif t > self.t_tot:
            print("Time is too large")
            sys.exit(-1)


def main():
    v = mph_to_mps(85)
    theta = np.deg2rad(30)
    phi = np.deg2rad(45)

    bb1 = battedBall(v, theta, phi, 0)
    bb1.printAttr()

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot(bb1.x_vec, bb1.y_vec, bb1.z_vec)

    ax.set_xlim3d(0, 100)
    ax.set_ylim3d(0, 100)
    ax.set_zlim3d(0, 50)

    ax.set_xlabel('1st Base Line')
    ax.set_ylabel('3rd Base Line')
    ax.set_zlabel('Height (Meters)')

    plt.show()

if __name__ == '__main__':
    main()
