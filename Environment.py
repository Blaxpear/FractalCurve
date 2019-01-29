import pygame
import time
from Graphics import Graphics
W = 512
H = 512

class Environment:
    """
    Class for handling pycharm
    """
    def __init__(self, root):
        pygame.init()
        pygame.display.set_caption("Fractal curve generator")
        self.surf = pygame.display.set_mode((W, H))
        self.exited = False
        self.graphics = Graphics(root, self.surf, (W/2, H/2))

    def mainloop(self):
        stage = 0
        time.sleep(2)
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