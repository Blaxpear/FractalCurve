import pygame
from math import pi
from CoordinateSpace import Coordinatespace
from CoordinateSpaceStack import CSStack
from Link import Link
from Toplink import TopLink


class Graphics:
    """
    Class for drawing
    """
    def __init__(self, root, surface, settings, debugger):
        """
        Initialize graphics
        :param root: the shape object that the fractal repeats
        :param surface: pygame surface object to draw on
        :param settings: reference to Settings object
        :param initialstage: initial stage
        """
        self.debug = debugger
        self.settings = settings
        self.clearframe = settings.getitem("Graphics", "clearframe", str) == "True"
        self.font = pygame.font.SysFont("Consolas", 12)
        self.draworigin = settings.getitem("Graphics", "draworigin", str) == "True"
        self.mirror = settings.getitem("Graphics", "mirror", str)
        self.colorstages = settings.getlist("Graphics", "colorstages", float)
        self.colors = settings.getlist2d("Graphics", "colors", float)
        self.root = root
        self.toplinks = []
        self.visuals = []
        self.stage = None
        self.surf = surface
        self.cs = Coordinatespace(0, 1, 1, (0, 0))
        self.csstack = CSStack(self.cs)
        self.screencs = None
        self.reset_view()

    def advancestage(self, amount, end):
        """
        Add amount to current stage. Clamp stage to end.
        """
        if end == -1:
            self.stage += amount
        else:
            self.stage = min(self.stage + amount, end)

    def redraw(self, new_toplinks):
        """
        Redraw fractal
        :param new_toplinks:
        if True, recalculate and assign top links
        if False, draw shapes onto top links
        """
        self.draw_bg()

        if new_toplinks:
            self.reset_toplinks()
            firstShape = self.root.draw(self.stage, self)
            if firstShape:
                # create a top link for the first shape
                self.add_toplink(Link(self.root.start,
                                      self.root.end,
                                      1,
                                      self.root,
                                      mirror_x=False,
                                      mirror_y=False))
        else:
            self.draw_toplinks()

        self.draw_stagecounter()

    def reset_view(self):
        """
        Reset view zoom and reset origin into ini file values
        :return:
        """
        angle = self.settings.getitem("Graphics", "angle", float)
        scale = self.settings.getitem("Graphics", "scale", float)
        originsetting = self.settings.getitem("Graphics", "origin", str)
        if originsetting == 'fit':
            d = self.root.length*scale
            res = self.settings.getlist("System", "resolution", int)
            x = (res[0] - d)/2
            y = res[1]/2
            origin = (x, y)
        else:
            origin = self.settings.getlist("Graphics", "origin", float)

        self.screencs = Coordinatespace(angle, scale, -scale, origin)

    def draw_bg(self):
        """
        Clear screen and draw origin if they are set true in settings
        """
        if self.clearframe:
            self.surf.fill((0, 0, 0))
        self.debug.origin()

    def draw_stagecounter(self):
        """
        Draw stage number to the top left corner
        """
        tesxsurf = self.font.render("{:.4f}".format(self.stage), False, (255, 255, 255))
        self.surf.blit(tesxsurf, (0,0))

    def draw_local(self, pos1, pos2, stage=None, color=None):
        """
        Draw a line using local coordinate system by converting pos1 and pos2 into global coordinates
        :param pos1: local point
        :param pos2: local point
        :param color: line color
        :param stage: stage for gradient coloring
        """
        self.debug.local_draw(self.cs, pos1, pos2)
        if color is None:
            color = self.get_gradient_color(stage)
        global_pos1 = self.cs.get_global_pos(pos1)
        global_pos2 = self.cs.get_global_pos(pos2)
        self.draw_global(global_pos1, global_pos2, color)
        if "y" in self.mirror or "x" in self.mirror:
            if "y" in self.mirror:
                global_pos1 = global_pos1[0], -global_pos1[1]
                global_pos2 = global_pos2[0], -global_pos2[1]
            if "x" in self.mirror:
                global_pos1 = -global_pos1[0], global_pos1[1]
                global_pos2 = -global_pos2[0], global_pos2[1]
            self.draw_global(global_pos1, global_pos2, color)

    def draw_global(self, pos1, pos2, color):
        """
        Draw line using global coordinate system
        :param pos1: global point
        :param pos2: global point
        :param color: line color
        """
        self.debug.global_draw(self.cs, pos1, pos2)
        screen_pos1 = self.screencs.get_global_pos(pos1)
        screen_pos2 = self.screencs.get_global_pos(pos2)
        pygame.draw.line(self.surf,
                         color,
                         (screen_pos1[0], screen_pos1[1]),
                         (screen_pos2[0], screen_pos2[1]),
                         1)


    def get_gradient_color(self, stage):
        """
        Get color from gradient at given stage.
        Gradient color changes linearly between two adjacent
        color stages and their corresponding color.
        If colors list contains only one color, return that
        :param stage: stage
        :return: [R, G, B] color from gradient at given stage
        """
        if len(self.colors) == 1:
            return self.colors[0]
        else:
            if stage == 1:
                return self.colors[-1]
            for i in range(len(self.colors)):
                if self.colorstages[i] <= stage < self.colorstages[i + 1]:
                    RGB1 = self.colors[i]
                    RGB2 = self.colors[i+1]
                    D_RGB = [RGB2[0] - RGB1[0],
                             RGB2[1] - RGB1[1],
                             RGB2[2] - RGB1[2]]
                    stageremainder = stage - self.colorstages[i]
                    stagegapsize = self.colorstages[i+1] - self.colorstages[i]
                    p = stageremainder/stagegapsize
                    r = min(max(0, RGB1[0] + D_RGB[0]*p), 255)
                    g = min(max(0, RGB1[1] + D_RGB[1]*p), 255)
                    b = min(max(0, RGB1[2] + D_RGB[2]*p), 255)
                    return r, g, b

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
        self.screencs.scale_by(p)

    def add_toplink(self, link):
        """
        Create a TopLink object from link
        :param link: link that draws the last shape at current stage
        """
        self.toplinks.append(TopLink(link.shape, self.cs, self.debug))

    def reset_toplinks(self):
        """
        Delete all elements in toplinks list.
        This needs to be executed every time stage passes whole numbers
        """
        self.toplinks = []

    def draw_toplinks(self):
        """
        Draw shapes onto top links.
        Top links must be assigned before calling this function.
        """
        self.csstack.push()
        for toplink in self.toplinks:
            toplink.draw(self.stage, self)
        self.csstack.revert()
        self.csstack.pop()
