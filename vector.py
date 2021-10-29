from __future__ import annotations
from math import cos, sin, sqrt, atan2


class Vector:
    def __init__(self, x: float, y: float, polar=False):
        self.x = x
        self.y = y

        if polar:
            self.x = x * sin(y)
            self.y = x * cos(y)

    @property
    def r(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    @property
    def theta(self) -> float:
        return atan2(self.x, self.y)

    def __abs__(self) -> float:
        return self.r

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __sub__(self, other: Vector) -> Vector:
        return self + (-other)

    def __mul__(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y

    def __matmul__(self, other: Vector) -> float:
        return self.x * other.y - other.x * self.y
