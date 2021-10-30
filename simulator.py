from math import pi, sin, sqrt, cos

from scipy.optimize import minimize_scalar

from field import Field
from fielder import Fielder
from vector import Vector


class Simulator:
    def __init__(self):
        self.field = Field(80)
        self.fielders = []

    def addFielder(self, fielder: Fielder):
        self.fielders.append(fielder)

    def fieldersInsideBoundary(self):
        return all([fielder.position.r <= self.field for fielder in self.fielders])

    def predictRuns(self, v: Vector):
        validFielders = []

        for fielder in self.fielders:
            # the relative angle between the ball's velocity and fielder position
            angle = v.theta - fielder.position.theta

            # this is the component of fielder velocity that is constant
            v_perp = abs(v * sin(angle))

            # check if the fielder can ever catch up with the ball without covering too much angular distance
            if v_perp <= fielder.v_max and abs(angle) < pi / 2:
                # this constraint is obtained using maximum fielder velocity
                v_parallel_max = sqrt(fielder.v_max ** 2 - v_perp ** 2)

                # this constraint is obtained using the boundary distance
                v_parallel_min = max(0, (v.r * fielder.position.r / self.field.radius) - v.r * cos(angle))

                # check if contraints are not contradictory
                if v_parallel_min < v_parallel_max:
                    # time needed for fielder to get to ball
                    def t(_v):
                        return fielder.position.r / (v.r * cos(angle) + _v)

                    # position of fielder when he gets to ball
                    def r(_v):
                        return v * t(_v)

                    # total time required to throw back the ball
                    def t_total(_v):
                        return t(_v) + min(r(_v).r, (r(_v) - self.field.nonStrikerEnd).r) / fielder.v_throw

                    # the runs that can be taken as a decimal value
                    def runs(_v):
                        return t_total(_v) / self.field.t_run

                    # probability of missfield, it is just a composition of missField function of fielder
                    def miss_field(_v):
                        return fielder.missField(sqrt(v_perp ** 2 + _v ** 2))

                    # the runs scored taking into account missfield
                    def runs_effective(_v):
                        return self.simulateNoFielders(_v) * miss_field(_v) + runs(_v) * (1 - miss_field(_v))

                    # HERE WE DEFINE SOME CONSTANTS ASSOCIATED WITH THE FIELDER AND BIND TO THE OBJECT
                    # minimize effective runs and find corresponding values of the functions defined above
                    v_parallel = minimize_scalar(runs_effective, bounds=(v_parallel_min, v_parallel_max),
                                                 method="bounded").x
                    fielder.v = sqrt(v_perp ** 2 + v_parallel ** 2)
                    fielder.t = t(v_parallel)
                    fielder.runs = runs(v_parallel)

                    validFielders.append(fielder)

        # sort the fielders in order of who gets to ball first
        validFielders.sort(key=lambda _f: _f.t)

        def effRunsRecursion(i):
            if i == len(validFielders):
                return self.simulateNoFielders(v.r)
            else:
                _f = validFielders[i]
                return _f.runs * (1 - _f.missField(_f.v)) + _f.missField(_f.v) * effRunsRecursion(i + 1)

        return effRunsRecursion(0)

    def simulateNoFielders(self, v):
        if v > self.field.v_min:
            return 4
        else:
            return 3
