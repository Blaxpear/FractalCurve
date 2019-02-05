import math


class Vertex:
    """
    Object that has position in the shape, and a position on a zero-shape
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x0 = None
        self.y0 = None
        self.dx = None
        self.dy = None

    def set_zeropos(self, x, y):
        """
        Set zero stage position
        :param x: x
        :param y: y
        """
        self.x0 = x
        self.y0 = y
        self.dx = self.x - self.x0
        self.dy = self.y - self.y0

    def pos(self, stage=1):
        """
        Return position of vertex in given stage
        :param stage: float from 0 to 1, 0 being the zero-shape position and 1 full shape
        :return: position as list: [x, y]
        """
        if stage == 0:
            # return zero-shape position
            return [self.x0, self.y0]
        elif stage >= 1:
            # full stage position
            return [self.x, self.y]
        else:
            # position in transition
            return [self.x0 + self.dx * stage, self.y0 + self.dy * stage]


    def angleTo(self, vertex):
        """
        Return angle between vector from this vertex to given vertex and positive x-axis
        :param vertex: vertex
        :return: float, angle in rads
        """
        return math.atan2(vertex.y - self.y, vertex.x - self.x)

    def distanceTo(self, vertex):
        """
        Return distance between vertices
        :param vertex: vertex
        :return: float, distance
        """
        return math.hypot(vertex.x - self.x, vertex.y - self.y)
