import pygame


class Graphics:
    """
    Class for drawing
    """
    def __init__(self, root):
        self.pg = pygame
        self.pg.init()
        self.pg.display.set_caption("Fractal curve generator")
        self.disp = self.pg.display.set_mode((512, 512))
        self.root = root

    def updatescreen(self, stage):
        """
        :param stage:
        stage of the fractal
        """
        self.disp.fill((0, 0, 0))
        self.root.draw(stage, self)
        self.pg.display.update()

    def draw_line(self, pos1, pos2):
        """
        draw a line using current coordinate system
        :param pos1:
        :param pos2:
        :return:
        """
        pygame.draw.line(self.disp,
                         (255, 255, 255),
                         (pos1[0], pos1[1]),
                         (pos2[0], pos2[1]),
                         1)
