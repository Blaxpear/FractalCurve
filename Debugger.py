from math import pi


class Debugger:
    """
    Class for printing and drawing information about the program
    """
    def __init__(self, settings):
        self.graphics = None
        self.enabled = settings.getitem("Debug", "enabled", str) == "True"
        self.drawing = settings.getitem("Debug", "drawing", str) == "True"
        self.toplinks = settings.getitem("Debug", "toplinks", str) == "True"
        self.origin_indicator = settings.getitem("Debug", "origin", str) == "True"

    def global_draw(self, cs, pos1, pos2):
        """
        Print details about coordinate space and points
        :param cs: coordinate space
        :param pos1: first point of line
        :param pos2: second point of line
        """
        if self.enabled and self.drawing:
            self.print_draw_info("GLOBAL", cs, pos1, pos2)

    def local_draw(self, cs, pos1, pos2):
        """
        Print details about coordinate space and points
        :param cs: coordinate space
        :param pos1: first point of line
        :param pos2: second point of line
        """
        if self.enabled and self.drawing:
            self.print_draw_info("LOCAL ", cs, pos1, pos2)

    @staticmethod
    def print_draw_info(scope, cs, pos1, pos2):
        print(scope + ":  scale: {:4.2f}, {:4.2f} angle: {:4.2f} orig: {:3}, {:3} pos1: {:3}, {:3} pos1: {:3}, {:3}"
              .format(cs.scale[0], cs.scale[1], cs.angle / 2 / pi * 360, cs.origin[0], cs.origin[1],
                      pos1[0], pos1[1], pos2[0], pos2[1]))

    def toplink(self, length):
        """
        Draw a white line from toplink origin to indicate x-axis direction
        :param length: length of the link
        """
        if self.enabled and self.toplinks:
            self.graphics.draw_local((0, 0), (length / 2, 0), 0, (255, 255, 255))

    def origin(self):
        """
        Draw x and y axis indicators at origin
        """
        if self.enabled and self.origin_indicator:
            # x
            self.graphics.draw_global((0, 0), (50, 0), color=(255, 0, 0))
            # y
            self.graphics.draw_global((0, 0), (0, 50), color=(0, 255, 0))
