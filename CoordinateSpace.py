import math


class Coordinatespace:
    """
    A transformed coordinate system
    """
    def __init__(self, angle, scale, origin):
        self.angle = angle
        self.scale = scale
        self.origin = origin

    def scale(self, factor):
        """
        Scale the local coordinate system from the local origin
        :param factor: scaling factor
        """
        self.scale *= factor

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


    def get_global_pos(self, pos):
        """
        Return global position from local pos
        :param pos:
        position in local coordinate system
        :return:
        global position
        """
        x, y = self.rotate_point(pos[0], pos[1], self.origin[0], self.origin[1], self.angle)

    @staticmethod
    def rotate_point(x, y, xo, yo, theta):
        """
        rotate x,y around xo,yo by theta (rad)
        :param x: x
        :param y: y
        :param xo: rotation origin x
        :param yo: rotation origin y
        :param theta: rotation angle
        :return:
        rotated positon
        """
        s = math.sin(theta)
        c = math.cos(theta)
        xr = c * (x-xo) - s * (y-yo) + xo
        yr = s * (x-xo) + c * (y-yo) + yo
        return [xr, yr]
