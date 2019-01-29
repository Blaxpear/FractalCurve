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
        self.link_adjacent()

    def link_adjacent(self):
        """
        Link each vertex to the one next to it
        """
        for i in range(len(self.vtx) - 1):
            self.links.append(self.link(self.vtx[i], self.vtx[i + 1]))

    def link(self, vtx1, vtx2):
        """
        Return a link between these vertices
        :param vtx1: first vertex
        :param vtx2: second vertex
        :return: Link object
        """
        d = vtx1.distanceTo(vtx2)
        scale = d / self.length
        return Link(vtx1, vtx2, scale, self)

    def draw(self, stage, graphics):
        graphics.csstack.push()
        if stage == 0:
            #draw zero-shape
            graphics.draw_line(self.vtx[0].pos(0), self.vtx[-1].pos(0))
        elif stage >= 1:
            next_stage = stage - 1
            for link in self.links:
                link.draw(next_stage, graphics)
                graphics.csstack.pop()
                graphics.csstack.revert()
        else:
            self.draw_transitional(stage, graphics)

    def draw_transitional(self, stage, graphics):
        for i in range(len(self.links)):
            graphics.draw_line(self.vtx[i].pos(stage), self.vtx[i+1].pos(stage))


