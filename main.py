from math import pi

from fielder import Fielder
from simulator import Simulator
from vector import Vector

sim = Simulator()
sim.addFielder(Fielder(Vector(50, 50*pi/180, polar=True)))
sim.addFielder(Fielder(Vector(30, 70*pi/180, polar=True)))
sim.addFielder(Fielder(Vector(10, 90*pi/180, polar=True)))
sim.addFielder(Fielder(Vector(60, 130*pi/180, polar=True)))
sim.addFielder(Fielder(Vector(70, 160*pi/180, polar=True)))
sim.addFielder(Fielder(Vector(36, 200*pi/180, polar=True)))
sim.addFielder(Fielder(Vector(71, 240*pi/180, polar=True)))
sim.addFielder(Fielder(Vector(38, 300*pi/180, polar=True)))

print(sim.predictRuns(Vector(20, 110*pi/180, polar=True)))
