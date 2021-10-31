from .vector import Vector


class Fielder:
    def __init__(self, pos, v_max=8, v_throw=25):
        self.position: Vector = Vector(pos[0], pos[1])
        # maximum running speed
        self.v_max = v_max
        # average throwing speed
        self.v_throw = v_throw
        self.missField = lambda speed: (speed / (v_max + 1)) ** 2

    def update_stat(self, pos=None, v_max=None, v_throw=None):
        if pos is not None: self.position = Vector(pos[0], pos[1])
        if v_max is not None: self.v_max = v_max
        if v_throw is not None: self.v_throw = v_throw
