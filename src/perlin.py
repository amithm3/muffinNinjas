import numpy as np
import numexpr as ne


class Perlin1D:
    def __init__(self, frequency=None, seed=None):
        if frequency is None:
            frequency = 8
        self.frequency = frequency
        self.amp = 360 / (frequency - 1)
        if seed is None:
            self.seed = np.random.randint(0, 2 ** 16)
        else:
            self.seed = seed
        np.random.seed(self.seed)
        self.fabric = np.random.uniform(0.7, 1, self.frequency).astype(np.float32)
        self.fabric[-1] = self.fabric[0]

        self.appender = [[[0]], [[1]]]

    def noise(self, x):
        atx = np.array([x]) / self.amp
        x = atx.astype(np.int32)
        index = (x + self.appender).transpose()
        atindex = self.fabric[index[:, 0]]

        return self.wrap(atindex, atx - x)

    @staticmethod
    def wrap(atindex, ata):
        ata = ata.astype(np.float32)
        return Perlin1D.smooth_wrap(ata) * (atindex[:, 1] - atindex[:, 0]) + atindex[:, 0]

    @staticmethod
    def smooth_wrap(a):
        return ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)")


class PerlinNoise1D:
    def __init__(self, octaves=None, seed=None, lacunarity=None, persistence=None):
        if lacunarity is None:
            lacunarity = 2
        if persistence is None:
            persistence = 0.5
        if octaves is None:
            octaves = 8
        self.octaves = octaves
        self.lacunarity = lacunarity
        self.persistence = persistence
        if seed is None:
            self.seed = np.random.randint(0, 2 ** 16)
        else:
            self.seed = seed
        self.perlins = [Perlin1D(self.lacunarity ** i, self.seed) for i in range(1, self.octaves + 1)]
        self.amplitude = [self.persistence ** i for i in range(1, self.octaves + 1)]

    def noise(self, x):
        return np.sum([self.perlins[i - 1].noise(x) * self.amplitude[i - 1] for i in range(1, self.octaves + 1)],
                      axis=0)
