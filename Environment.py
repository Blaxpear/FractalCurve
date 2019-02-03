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
        self.surf = pygame.display.set_mode(settings.getlist("System", "resolution", int))
        self.exited = False
        self.graphics = Graphics(root, self.surf, settings)

    def mainloop(self):
        """
        Animate fractal until window is closed
        """
        stage = 0
        while not self.exited:
            stage += 0.01
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
