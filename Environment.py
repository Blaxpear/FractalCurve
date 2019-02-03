import pygame
import time
from Graphics import Graphics

class Environment:
    """
    Class for handling pycharm
    """
    def __init__(self, root, settings):
        """
        Initialize environment
        :param root: Shape to make the fractal from
        """
        pygame.init()
        pygame.display.set_caption("Fractal curve generator")
        self.settings = settings
        self.surf = pygame.display.set_mode(settings.getlist("System", "resolution", int))
        self.exited = False
        self.graphics = Graphics(root, self.surf, settings)

    def runmode(self):
        mode = self.settings.getitem("Program", "mode", str)
        if mode == "animate":
            initial = self.settings.getitem("Program", "initialstage", float)
            end = self.settings.getitem("Program", "endstage", float)
            speed = self.settings.getitem("Program", "speed", float)
            self.animate(initial, end, speed)
        elif mode == "image":
            stage = self.settings.getitem("Program", "endstage", float)
            self.image(stage)

    def image(self, stage):
        """
        draw image of the fractal at given stage
        :param stage: stage
        """
        while not self.exited:
            self.doevents()
            self.graphics.redraw(stage)
            pygame.display.update()

    def animate(self, start, end, speed):
        """
        Animate fractal stages from start to end
        :param start: first stage
        :param end: last stage, -1 for infinity
        :param speed: how much stage changes each frame
        """
        stage = start
        while not self.exited and (stage <= end or end == -1):
            stage += speed
            self.doevents()
            self.graphics.redraw(stage)
            pygame.display.update()
            time.sleep(0.01)

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
                    self.graphics.resetview()
