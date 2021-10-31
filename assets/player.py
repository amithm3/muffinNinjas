# <<<the following file generates random batsman statistics>>>
import csv

from numpy import hstack
from numpy.random import normal

with open("players/default/speed.csv", "w+", newline='') as f:
    data = hstack((normal(loc=20, scale=5, size=10),
                   normal(loc=15, scale=10, size=5),
                   normal(loc=25, scale=5, size=20)))

    writer = csv.writer(f)

    for i in data:
        writer.writerow([i])

with open("players/default/angle.csv", "w+", newline='') as f:
    data = hstack((normal(loc=10, scale=40, size=10),
                   normal(loc=70, scale=10, size=20),
                   normal(loc=110, scale=20, size=40),
                   normal(loc=170, scale=12, size=5),
                   normal(loc=240, scale=30, size=20),
                   normal(loc=300, scale=30, size=10)))

    writer = csv.writer(f)

    for i in data:
        writer.writerow([i])
