from Link import Link


class Shape:
    """
    Object that is the repeating pattern in the fractal
    """
    def __init__(self, vtxlist):
        """
        Create shape by linking adjacent vertices in the vtxlist
        :param vtxlist: list of vertices
        """
        self.length = vtxlist[0].distanceTo(vtxlist[-1])
        self.links = []
        self.vtx = vtxlist

    def link(self, vtx1, vtx2):
        """
        Return a link between these vertices
        :param vtx1: first vertex
        :param vtx2: second vertex
        :return: Link object
        """
        d = vtx1.distanceTo(vtx2)
        scale = d / self.length
        return Link(vtx1, vtx2, scale)

    def draw(self, stage, graphics):
        graphics.csstack.push()
        if stage == 0:
            #draw zero-shape
            graphics.draw_line(self.vtx[0].pos(0), self.vtx[-1].pos(0))
        else:
            #TODO: draw shape
            print("draw non-zero shape")
