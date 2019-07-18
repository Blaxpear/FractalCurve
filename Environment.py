import pygame
import time
import imageio
from os import listdir, remove
from os.path import isfile, join
from math import ceil
from Graphics import Graphics


class Environment:
    """
    Class for handling pycharm
    """
    def __init__(self, root, settings, debugger):
        """
        Initialize environment
        :param root: Shape to make the fractal from
        :param settings: reference to Settings object
        :param debugger: reference to Debugger object
        """
        pygame.init()
        pygame.display.set_caption("Fractal curve generator")

        self.settings = settings
        self.surf = pygame.display.set_mode(settings.getlist("System", "resolution", int))
        self.exited = False
        self.graphics = Graphics(root, self.surf, settings, debugger)
        self.debug = debugger
        self.debug.graphics = self.graphics
        self.total_lines = 0
        self.autodraw = settings.getitem("Program", "autodraw", str) == "True"
        self.premature = settings.getitem("Program", "premature", str) == "True"
        self.shapes = settings.getitem("Program", "shapes", int)
        self.export = settings.getitem("Program", "export", str) == "True"

    def runmode(self):
        """
        Run mode defined in settings
        """
        endstage = self.settings.getitem("Program", "endstage", float)
        self.total_lines = self.linestodraw(endstage)
        print("Total lines:", self.total_lines)
        mode = self.settings.getitem("Program", "mode", str)
        if mode == "animate":
            initial = self.settings.getitem("Program", "initialstage", float)
            speed = self.settings.getitem("Program", "speed", float)
            self.animate(initial, endstage, speed)
        elif mode == "image":
            self.image(endstage)

    def image(self, stage):
        """
        draw image of the fractal at given stage
        :param stage: stage
        """
        self.graphics.stage = stage
        while not self.exited:
            self.updateFrame()


    def animate(self, start, end, speed):
        """
        Animate the fractal
        :param start: first stage
        :param end: last stage, -1 for infinity
        :param speed: how much stage changes each frame
        """
        self.graphics.stage = start
        while not self.exited:
            if self.graphics.stage <= end or end == -1:
                self.graphics.advancestage(speed, end)
                self.updateFrame()

            if self.export:
                self.exportScreen("tmp", self.graphics.stage)

            time.sleep(0.01)

        if self.export:
            self.exportToGif("animation.gif")

    def updateFrame(self):
        """
        Handle events for a new frame
        """
        self.doevents()
        if self.autodraw:
            self.graphics.redraw(self.premature, self.shapes)
        pygame.display.update()

    def exportToGif(self, name):
        files = [f for f in listdir("./tmp") if isfile(join("./tmp", f))]
        images = []
        for file in files:
            images.append(imageio.imread('./tmp/'+file))
            remove('./tmp/'+file)
        imageio.mimsave(name, images, duration=0.001)

    def exportScreen(self, folder, stage):
        pygame.image.save(self.surf, "{}/frame{}.jpeg".format(folder, stage))

    def linestodraw(self, stage):
        """
        Return number of lines required to draw fractal at the given stage
        :param stage: stage
        :return: int, number of lines
        """
        linesinshape = len(self.graphics.root.links + self.graphics.root.visuals)
        return linesinshape ** ceil(stage)

    def print_progress(self):
        """
        Print the percetage of lines being drawn now compared to
        the amount of lines to be drawn when last stage has been
        reached.
        """
        n_drawn = self.linestodraw(self.graphics.stage)
        print("{:.10f}%".format(float(n_drawn/self.total_lines)))

    def doevents(self):
        """
        handle pygame events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exited = True
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] == 1:
                    self.graphics.drag_screen(event.rel)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.graphics.zoom_screen(1.1)
                elif event.button == 5:
                    self.graphics.zoom_screen(1/1.1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.graphics.reset_view()
                if event.key == pygame.K_F5:
                    self.graphics.redraw()
