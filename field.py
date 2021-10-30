from vector import Vector


class Field:
    def __init__(self, radius: float):
        # <<<CODE FOR CUSTOM BOUNDARY>>>
        # """
        # boundary is an array of Vectors representing the boundary of the field
        # the exact boundary is found via interpolation
        # """
        # # the following code works by magic
        # self.x = []
        # self.y = []
        #
        # for vec in boundary:
        #     self.x.append(vec.x)
        #     self.y.append(vec.y)
        #
        # self.x.append(self.x[0])
        # self.y.append(self.y[0])
        #
        # self.tck, u = interpolate.splprep([self.x, self.y], s=0, per=True)
        #
        # self.boundary = interpolate.splev(np.linspace(0, 1, res), self.tck)

        self.radius = radius

        # position of non striker end
        self.nonStrikerEnd = Vector(0, -20)

        # time required to take a run
        self.t_run = 3

        # minimum velocity for ball to reach the ropes
        self.v_min = 15

    # <<<CODE FOR PLOTTING CUSTOM BOUNDARY>>>
    # def plotBoundary(self):
    #     fig, ax = plt.subplots(1, 1)
    #     ax.plot(self.x, self.y, 'or')
    #     ax.plot(*self.boundary, '-b')
    #
    #     plt.show()
