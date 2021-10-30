from __future__ import annotations
from math import cos, sin, sqrt, atan2
import copy


class Vector:
    def __init__(self, x: float, y: float, polar=False):
        self.x = x
        self.y = y

        # we are taking angles with respect to y axis rather than the conventional x axis
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

    def __mul__(self, other: float) -> Vector:
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> Vector:
        return self * other

    def __truediv__(self, other: float) -> Vector:
        return self * (1 / other)

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vector) -> float:
        return self.x * other.y - other.x * self.y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    # copy function
    def copy(self) -> Vector:
        return copy.copy(self)
