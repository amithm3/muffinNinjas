from math import pi
from numpy.random import normal
from numpy import hstack

from src.fielder import Fielder
from src.simulator import Simulator
from vector import Vector

sim = Simulator()

# Add as many fielder as you wish
sim.addFielder(Fielder(Vector(50, 50 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(30, 70 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(10, 90 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(60, 130 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(70, 160 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(36, 200 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(71, 240 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(38, 300 * pi / 180, polar=True)))

# predict the runs scored for a particular shot
print(sim.predictRuns(Vector(20, 110 * pi / 180, polar=True)))

# input some of the batsman's data
sim.inputData(speed=hstack((normal(loc=20, scale=5, size=10),
                            normal(loc=15, scale=10, size=5),
                            normal(loc=25, scale=5, size=20))),

              angle=hstack((normal(loc=10 * pi / 180, scale=40 * pi / 180, size=10),
                            normal(loc=70 * pi / 180, scale=10 * pi / 180, size=20),
                            normal(loc=110 * pi / 180, scale=20 * pi / 180, size=40),
                            normal(loc=170 * pi / 180, scale=12 * pi / 180, size=5),
                            normal(loc=240 * pi / 180, scale=30 * pi / 180, size=20),
                            normal(loc=300 * pi / 180, scale=30 * pi / 180, size=10))))

# get the rating of the field based on the data
print(sim.rate())
