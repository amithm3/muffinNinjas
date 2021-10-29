from math import pi

from field import Field
from vector import Vector


boundaryLine = Field((Vector(70, 0 * pi / 180, polar=True),
                      Vector(80, 30 * pi / 180, polar=True),
                      Vector(81, 60 * pi / 180, polar=True),
                      Vector(82, 90 * pi / 180, polar=True),
                      Vector(72, 120 * pi / 180, polar=True),
                      Vector(70, 150 * pi / 180, polar=True),
                      Vector(80, 180 * pi / 180, polar=True),
                      Vector(82, 210 * pi / 180, polar=True),
                      Vector(83, 240 * pi / 180, polar=True),
                      Vector(76, 270 * pi / 180, polar=True),
                      Vector(80, 300 * pi / 180, polar=True),
                      Vector(80, 330 * pi / 180, polar=True)))

boundaryLine.plot()
