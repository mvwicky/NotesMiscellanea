import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import random


def monteCarloInt(nSamps, coeffs, xMin, xMax):
    hit = 0
    yMin = 0
    yMax = 0
    xVec = []
    yVec = []

    for i in range(len(coeffs)):
        yMax += (xMax**i)*coeffs[i]

    area = xMax * yMax
    random.seed()
    for i in range(nSamps):
        x = random.uniform(xMin, xMax)
        y = random.uniform(yMin, yMax)
        res = 0
        for j in range(len(coeffs)):
            res += (x**j) * coeffs[j]
        if y <= res:
            hit += 1
        xVec.append(x)
        yVec.append(y)

    aBar = (hit / nSamps)*area
    return xVec, yVec, aBar


def compFunc(x, coeffs):
    ret = 0
    for i in range(len(coeffs)):
        ret += (x**i)*coeffs[i]
    return ret


def main():
    xMin = 0
    xMax = 10
    N = 2500
    coeffs = [7, 6, 4]
    xVec, yVec, aBar = monteCarloInt(N, coeffs, xMin, xMax)

    nn = np.linspace(0, xMax, N)
    f = []
    for i in nn:
        f.append(compFunc(i, coeffs))

    print(aBar)
    plt.plot(xVec, yVec, '.', nn, f, lw=4)
    plt.show()

if __name__ == '__main__':
    main()
