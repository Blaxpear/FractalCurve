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
        self.vtx = vtxlist
        self.set_zeroshape()
        self.links = []
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
        """
        Draw shape in given stage
        :param stage: stage
        :param graphics: graphics object to draw onto
        """
        if stage == 0:
            # draw zero-shape, aka a line from first to last vertex
            graphics.draw_line(self.vtx[0].pos(0), self.vtx[-1].pos(0), stage)
        elif stage < 1:
            self.draw_transitional(stage, graphics)
        else:
            # push coordinate system of this shape
            graphics.csstack.push()

            next_stage = stage - 1
            for link in self.links:
                link.draw(next_stage, graphics)
                # revert coordinate space that was altered by the link
                # to equal the coordinate space of this shape
                graphics.csstack.revert()
            # remove the coordinate space of this shape from the stack
            graphics.csstack.pop()


    def draw_transitional(self, stage, graphics):
        """
        Draw the shape in transition from a line to the full shape
        :param stage: stage
        :param graphics: graphics object to draw onto
        """
        for i in range(len(self.links)):
            graphics.draw_line(self.vtx[i].pos(stage), self.vtx[i+1].pos(stage), stage)

    def set_zeroshape(self):
        """
        Set zero shape position for each vertex
        """
        vtxamount = len(self.vtx)
        dx = self.length/(vtxamount-1)
        for i in range(vtxamount):
            self.vtx[i].set_zeropos(i*dx, 0)
