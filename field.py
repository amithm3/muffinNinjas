from typing import Iterable

import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

from vector import Vector


class Field:
    def __init__(self, boundary: Iterable[Vector], res=100):
        """
        boundary is an array of Vectors representing the boundary of the field
        the exact boundary is found via interpolation
        """
        # the following code works by magic
        self.x = []
        self.y = []

        for vec in boundary:
            self.x.append(vec.x)
            self.y.append(vec.y)

        self.x.append(self.x[0])
        self.y.append(self.y[0])

        self.tck, u = interpolate.splprep([self.x, self.y], s=0, per=True)

        self.boundary = interpolate.splev(np.linspace(0, 1, res), self.tck)

    def plot(self):
        fig, ax = plt.subplots(1, 1)
        ax.plot(self.x, self.y, 'or')
        ax.plot(*self.boundary, '-b')

        plt.show()
