import pygame
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
        while not self.exited:
            self.doevents()
            self.graphics.redraw(0)
            pygame.display.update()

    def doevents(self):
        """
        handle pygame events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exited = True