import pygame
from CoordinateSpace import Coordinatespace
from CoordinateSpaceStack import CSStack


class Graphics:
    """
    Class for drawing
    """
    def __init__(self, root, surface, settings):
        """
        Initialize graphics
        :param root: first shape to draw
        :param surface: pygame surface object to draw on
        :param origin: (x, y) position of the root. default: (0, 0), top left corner
        """
        self.root = root
        self.surf = surface
        self.settings = settings
        self.cs = Coordinatespace(settings.angle, settings.scale, settings.origin)
        self.csstack = CSStack(self.cs)

    def redraw(self, stage):
        """
        Clear surface and redraw fractal
        :param stage: stage of the fractal
        """
        self.draw_bg()
        self.root.draw(stage, self)
        self.csstack.pop()

    def draw_bg(self):
        """
        Clear screen and draw origin
        """
        self.surf.fill((0,0,0))
        self.draw_origin()

    def draw_origin(self):
        """
        Draw a 20 by 20 red cross in the origin
        """
        self.draw_line((0, 10), (0,-10), color=(255, 0, 0))
        self.draw_line((10, 0), (-10, 0), color=(255, 0, 0))

    def draw_line(self, pos1, pos2, color=None, stage=None):
        """
        Draw a line using local coordinate system by converting pos1 and pos2 into global coordinates
        :param pos1: local point
        :param pos2: local point
        :param color: line color
        """
        if color is None:
            color = self.get_gradient_color(stage)
        global_pos1 = self.cs.get_global_pos(pos1)
        global_pos2 = self.cs.get_global_pos(pos2)
        pygame.draw.line(self.surf,
                         color,
                         (global_pos1[0], global_pos1[1]),
                         (global_pos2[0], global_pos2[1]),
                         1)

    def get_gradient_color(self, stage):
        """
        Get color from settings.gradient using settings.gradientbounds
        :param stage: stage
        :return: [R, G, B] color from gradient
        """
        RGB1 = self.settings.gradient[0]
        RGB2 = self.settings.gradient[1]
        D_RGB = [RGB2[0] - RGB1[0], RGB2[1] - RGB1[1], RGB2[2] - RGB1[2]]
        p = min(stage/self.settings.gradientbounds, 1)
        return [RGB1[0] + D_RGB[0]*p, RGB1[1] + D_RGB[1]*p, RGB1[2] + D_RGB[2]*p]
