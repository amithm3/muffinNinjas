import csv
from math import radians

import numpy as np
from scipy import interpolate, optimize
from matplotlib import pyplot as plt

from .vector import Vector


class Field:
    def __init__(self, path=None):
        # the file contains data in degrees format
        if path:
            self.load(path)

    def load(self, path):
        """
        load csv file contains data with degree format
        """
        self.boundaryVectors = []

        self.x = []
        self.y = []

        with open(path, 'r', newline='') as f:
            for row in csv.reader(f):
                v = Vector(float(row[0]), radians(float(row[1])), polar=True)
                self.boundaryVectors.append(v)
                self.x.append(v.x)
                self.y.append(v.y)

        x = self.x + [self.x[0]]
        y = self.y + [self.y[0]]

        self.tck, self.u = interpolate.splprep([x, y], s=0, per=True)

    def evaluate(self, t) -> Vector:
        """
        evaluates the boundary at given parameter
        """
        x, y = interpolate.splev([t], self.tck)
        return Vector(x[0], y[0])

    def boundaryLength(self, theta, degrees=True):
        """
        returns length of boundary at given angle
        """
        def f(t):
            v = self.evaluate(t)
            if degrees:
                return radians(theta) - v.theta
            else:
                return theta - v.theta

        sol = optimize.root_scalar(f, x0=0.5, x1=0.3)

        return self.evaluate(sol.root).r

    def plot(self):
        """
        use matplotlib to plot boundary approximation
        """
        fig, ax = plt.subplots(1, 1)
        ax.plot(self.x, self.y, 'or')
        print(interpolate.splev([0.5], self.tck))
        ax.plot(*interpolate.splev(np.linspace(0, 1, 1000), self.tck), '-b')

        plt.show()
