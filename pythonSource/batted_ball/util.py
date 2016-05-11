import numpy as np


meters_per_mile = 1609.34


def mph_to_mps(mph):
    return mph * (meters_per_mile / 60**2)


def deg_to_rad(deg):
    return deg * (np.pi / 180)


def gcd(a, b):
    a = int(a)  # ensure a and b and integers
    b = int(b)
    while (b != 0):
        t = b
        b = a % b
        a = t
    return a


def calc_e(n):  # calculate e for n iterations
    ret = 0
    for i in range(n):
        ret += 1 / np.math.factorial(i)
    return ret


def calc_pi(n):  # calculate pi for n iteration (sharp formula)
    ret = 0
    for i in range(n):
        ret += (2 * -1**i * 3**(0.5 - i)) / (2 * k + 1)
    return ret


def q_pochhammer(a, q, k):
    ret = 0
    if k > 0:
        for i in range(k):
            ret *= 1 - a * q**i
    elif k == 0:
        ret = 1
    elif k < 0:
        for i in range(1, np.math.absolute(k)+1):
            ret *= (1 - a * q**-i)**-1
    return ret
