from math import pi, sin, sqrt, cos

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
        v_parallel_ranges = []
        t_field_functions = []

        for fielder in self.fielders:
            angle = v.theta - fielder.position.theta
            v_perp = abs(v * sin(angle))

            if v_perp <= fielder.v_max and abs(angle) < pi / 2:
                v_parallel_max = sqrt(fielder.v_max**2 - v_perp**2)

                v_parallel_min = max(0, (v.r * fielder.position.r / self.field.radius) - v.r * cos(angle))

                if v_parallel_min < v_parallel_max:
                    validFielders.append(fielder)
                    v_parallel_ranges.append((v_parallel_min, v_parallel_max))

                    # time needed for fielder to get to ball
                    t_field = lambda _v: fielder.position.r / (v.r * cos(angle) + _v)

                    # position of fielder when he gets to ball
                    r_field = lambda _v: v * t_field(_v)

                    # total time required to throw back the ball
                    t_total = lambda _v: t_field(_v) + min(r_field(_v).r, (r_field(_v) - self.field.nonStrikerEnd).r) / fielder.v_throw

                    # the runs that can be taken
                    runs = lambda _v: t_field(_v) / self.field.t_run

                    runs_min = runs(v_parallel_max)
                    runs_max = runs(v_parallel_min)

                    print(runs_min, runs_max)
