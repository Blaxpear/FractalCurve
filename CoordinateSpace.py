import math


class Coordinatespace:
    """
    A transformed coordinate system
    """
    def __init__(self, angle, scale, origin):
        self.angle = angle
        self.s = [scale, scale]
        self.origin = origin

    def scale(self, factor):
        """
        Scale the local coordinate system from the local origin
        :param factor: scaling factor
        """
        self.s = [self.s[0]*factor, self.s[1]*factor]

    def scale_x(self, factor):
        """
        Scale the local x axis
        :param factor: scaling factor
        """
        self.s[0] = self.s[0]*factor

    def scale_y(self, factor):
        """
        Scale the local y axis
        :param factor: scaling factor
        """
        self.s[1] = self.s[1]*factor

    def rotate(self, theta):
        """
        Rotate the local coordinate space around local origin
        :param theta: rotation angle
        """
        self.angle += theta

    def set_origin(self, pos):
        """
        Set coordinate system origin to pos
        :param pos:
        position in local coordinate system
        """
        self.origin = self.get_global_pos(pos)

    def make_equal(self, other):
        """
        Copy angle scale and origin from given coordinate space
        :param other: coordinate space to copy
        """
        self.angle = other.angle
        self.s = other.s
        self.origin = other.origin

    def get_global_pos(self, pos):
        """
        Return global position from local pos.
        Rotate, scale and translate the local pos to get the global position.
        :param pos:
        (x, y) position in local coordinate system
        :return:
        (x, y) global position
        """
        x, y = self.rotate_point(pos[0], pos[1], 0, 0, self.angle)
        return self.origin[0] + x*self.s[0], self.origin[1] + y*self.s[1]

    @staticmethod
    def rotate_point(x, y, xo, yo, theta):
        """
        rotate x,y around xo,yo by theta (rad)
        :param x: x
        :param y: y
        :param xo: rotation origin x
        :param yo: rotation origin y
        :param theta: rotation angle
        :return: rotated positon
        """
        s = math.sin(theta)
        c = math.cos(theta)
        xr = c * (x-xo) - s * (y-yo) + xo
        yr = s * (x-xo) + c * (y-yo) + yo
        return [xr, yr]
