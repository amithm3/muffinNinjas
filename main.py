from math import radians

from src.fielder import Fielder
from src.simulator import Simulator
from src.vector import Vector


sim = Simulator()

# load the field from a csv file
sim.field.load("assets/fields/default.csv")

# Add as many fielder as you wish
sim.addFielder(Fielder(Vector(50, radians(50), polar=True)))
sim.addFielder(Fielder(Vector(30, radians(70), polar=True)))
sim.addFielder(Fielder(Vector(10, radians(90), polar=True)))
sim.addFielder(Fielder(Vector(60, radians(130), polar=True)))
sim.addFielder(Fielder(Vector(70, radians(160), polar=True)))
sim.addFielder(Fielder(Vector(36, radians(200), polar=True)))
sim.addFielder(Fielder(Vector(71, radians(240), polar=True)))
sim.addFielder(Fielder(Vector(38, radians(300), polar=True)))

# check that fielders are inside the boundary
print(sim.fieldersInsideBoundary())

# input some of the batsman's data
sim.inputData("assets/players/default/speed.csv", "assets/players/default/angle.csv")

# predict the runs scored for a particular shot
print(sim.predictRuns(Vector(20, radians(110), polar=True)))

# get the rating of the field based on the data
print(sim.rate())
