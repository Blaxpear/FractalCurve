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
        :param settings: settings object
        :param initialstage: initial stage
        """
        self.clearframe = settings.getitem("Graphics", "clearframe", str) == "True"
        self.root = root
        self.stage = 0
        self.surf = surface
        self.settings = settings
        self.cs = Coordinatespace(0, 1, (0, 0))
        self.csstack = CSStack(self.cs)
        self.resetview()
        self.font = pygame.font.SysFont("Consolas", 12)
        self.draworigin = settings.getitem("Graphics", "draworigin", str) == "True"

    def resetview(self):
        """
        Reset view zoom and pan into ini file values
        :return:
        """
        self.screencs = Coordinatespace(self.settings.getitem("Graphics", "angle", float),
                                        self.settings.getitem("Graphics", "scale", float),
                                        self.settings.getlist("Graphics", "origin", float))

    def advancestage(self, amount):
        """
        Add amount to current stage
        """
        self.stage += amount

    def redraw(self):
        """
        Clear surface and redraw fractal
        """
        self.draw_bg()
        self.root.draw(self.stage, self)
        self.drawstagecounter()
        self.csstack.pop()

    def draw_bg(self):
        """
        Clear screen and draw origin
        """
        if self.clearframe:
            self.surf.fill((0, 0, 0))
        if self.draworigin:
            self.draw_origin()

    def draw_origin(self):
        """
        Draw a 20 by 20 red cross in the origin
        """
        self.draw_line((0, 10), (0,-10), color=(255, 0, 0))
        self.draw_line((10, 0), (-10, 0), color=(255, 0, 0))

    def drawstagecounter(self):
        """
        Draw stage number to the top left corner
        """
        tesxsurf = self.font.render("{:.4f}".format(self.stage), False, (255, 255, 255))
        self.surf.blit(tesxsurf, (0,0))

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

    def draw_line(self, pos1, pos2, stage, color=None):
        """
        Draw a line using local coordinate system by converting pos1 and pos2 into global coordinates
        :param pos1: local point
        :param pos2: local point
        :param color: line color
        :param stage: stage for gradient coloring
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
        Get color from gradient.
        Gradient changes linearly between two adjacent colorstages and their corresponding color.
        :param stage: stage
        :return: [R, G, B] color from gradient at given stage
        """
        colorstages = self.settings.getlist("Graphics", "colorstages", float)
        colors = self.settings.getlist2d("Graphics", "colors", float)
        if len(colors) == 1:
            return colors[0]
        else:
            if stage == 1:
                return colors[-1]
            for i in range(len(colors)):
                if colorstages[i] <= stage < colorstages[i + 1]:
                    RGB1 = colors[i]
                    RGB2 = colors[i+1]
                    D_RGB = [RGB2[0] - RGB1[0], RGB2[1] - RGB1[1], RGB2[2] - RGB1[2]]
                    stageremainder = self.stage - colorstages[i]
                    stagegapsize = colorstages[i+1] - colorstages[i]
                    p = stageremainder/stagegapsize
                    r = min(max(0, RGB1[0] + D_RGB[0]*p), 255)
                    g = min(max(0, RGB1[1] + D_RGB[1]*p), 255)
                    b = min(max(0, RGB1[2] + D_RGB[2]*p), 255)
                    return [r, g, b]
