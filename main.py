from math import pi

from fielder import Fielder
from simulator import Simulator
from vector import Vector

sim = Simulator()

# load the field from a csv file
sim.field.load("resources/fields/default.csv")

# Add as many fielder as you wish
sim.addFielder(Fielder(Vector(50, 50 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(30, 70 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(10, 90 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(60, 130 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(70, 160 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(36, 200 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(71, 240 * pi / 180, polar=True)))
sim.addFielder(Fielder(Vector(38, 300 * pi / 180, polar=True)))

# check that fielders are inside the boundary
print(sim.fieldersInsideBoundary())

# input some of the batsman's data
sim.inputData("resources/players/default/speed.csv", "resources/players/default/angle.csv")

# predict the runs scored for a particular shot
print(sim.predictRuns(Vector(20, 110 * pi / 180, polar=True)))

# get the rating of the field based on the data
print(sim.rate())
