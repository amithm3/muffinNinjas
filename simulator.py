from math import pi, sin, sqrt, cos, ceil, floor

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
        effective_run_list = []
        t_field_list = []

        for fielder in self.fielders:
            angle = v.theta - fielder.position.theta
            v_perp = abs(v * sin(angle))

            if v_perp <= fielder.v_max and abs(angle) < pi / 2:
                v_parallel_max = sqrt(fielder.v_max**2 - v_perp**2)

                v_parallel_min = max(0, (v.r * fielder.position.r / self.field.radius) - v.r * cos(angle))

                if v_parallel_min < v_parallel_max:
                    # time needed for fielder to get to ball
                    t_field = lambda _v: fielder.position.r / (v.r * cos(angle) + _v)

                    # inverse of above function
                    t_field_inv = lambda _t: (fielder.position.r / _t) - v.r * cos(angle)

                    # position of fielder when he gets to ball
                    r_field = lambda _v: v * t_field(_v)

                    # total time required to throw back the ball
                    t_total = lambda _v: t_field(_v) + min(r_field(_v).r, (r_field(_v) - self.field.nonStrikerEnd).r) / fielder.v_throw

                    # the runs that can be taken as a decimal value, we will eventually use the floor
                    runs = lambda _v: t_field(_v) / self.field.t_run

                    runs_min = runs(v_parallel_max)
                    runs_max = runs(v_parallel_min)

                    # probability of missfield
                    miss_field = lambda _v: fielder.missField(sqrt(v_perp ** 2 + _v ** 2))
                    effective_runs = lambda _v: self.simulateNoFielders(_v) * miss_field(_v) + runs(_v) * (1 - miss_field(_v))

                    solution = minimize_scalar(effective_runs, bounds=(v_parallel_min, v_parallel_max), method="bounded")
                    v_parallel = solution.x

                    validFielders.append(fielder)

                    print(runs_min, runs_max, runs(v_parallel))

        if len(validFielders) == 0:
            return self.simulateNoFielders(v.r)

    def simulateNoFielders(self, v):
        if v > self.field.v_min:
            return 4
        else:
            return 3
