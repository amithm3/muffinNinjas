from vector import Vector


class Fielder:
    def __init__(self, pos: Vector, v_max=8, v_throw=25):
        self.position: Vector = pos
        # maximum running speed
        self.v_max = v_max
        # average throwing speed
        self.v_throw = v_throw
        self.missField = lambda speed: (speed / (v_max + 1)) ** 2
