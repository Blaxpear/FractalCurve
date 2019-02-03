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
        self.screencs = Coordinatespace(0, 1, settings.origin)
        self.cs = Coordinatespace(settings.angle, settings.scale, (0, 0))
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

    def drag_screen(self, amount):
        """
        Move screen coordinate space origin by amount. In other words drag the whole screen by amount.
        :param amount: (dx, dy)
        """
        o = self.screencs.origin
        self.screencs.origin = (o[0] + amount[0], o[1] + amount[1])

    def zoom_screen(self, p):
        """
        Scale screen coordinate space by p.
        :param p: percentage to scale.
        Examples
        p = 1: 100%, nothing happens
        p = 2: 200%, zoom in to twice the current scale
        p = 0.5: 50%, zoom out to half the current scale
        """
        #TODO: zoomin into a point
        self.screencs.scale(p)

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
        screen_pos1 = self.screencs.get_global_pos(global_pos1)
        screen_pos2 = self.screencs.get_global_pos(global_pos2)
        pygame.draw.line(self.surf,
                         color,
                         (screen_pos1[0], screen_pos1[1]),
                         (screen_pos2[0], screen_pos2[1]),
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
