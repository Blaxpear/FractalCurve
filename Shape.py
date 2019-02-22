from Link import Link


class Shape:
    """
    Object that is the repeating pattern in the fractal
    """
    def __init__(self):
        self.length = None
        self.start = None
        self.end = None
        # list of Link objects that will recursively draw next shapes
        self.links = None
        # list of Vertex object pairs to only draw lines
        self.visuals = None

    def link_vertices(self, vtxlist):
        self.length = vtxlist[0].distanceTo(vtxlist[-1])
        self.start = vtxlist[0]
        self.end = vtxlist[-1]
        self.set_zeroshape(vtxlist)
        self.links = []
        self.link_adjacent(vtxlist)
        self.visuals = []

    def link_adjacent(self, vtxlist):
        """
        Link each vertex to the one next to it
        """
        for i in range(len(vtxlist) - 1):
            if i % 2 == 0:
                self.links.append(self.link(vtxlist[i], vtxlist[i + 1], mirror_y=True, mirror_x=False))
            else:
                self.links.append(self.link(vtxlist[i], vtxlist[i + 1], mirror_y=False, mirror_x=False))

    def link(self, vtx1, vtx2, mirror_x, mirror_y) -> Link:
        """
        Return a link between these vertices
        :param vtx1: first vertex
        :param vtx2: second vertex
        :return: Link object
        """
        d = vtx1.distanceTo(vtx2)
        scale = d / self.length
        return Link(vtx1, vtx2, scale, self, mirror_x=mirror_x, mirror_y=mirror_y)

    def draw(self, stage, graphics) -> bool:
        """
        Draw shape in given stage and assign top links
        :param stage: stage
        :param graphics: graphics object
        :return: True if this was the last shape to draw
        """
        if stage == 0:
            # draw zero-shape, aka a line from first to last vertex
            graphics.draw_local(self.start.pos(0), self.end.pos(0), stage)
            return True
        elif stage <= 1:
            self.draw_transitional(stage, graphics)
            return True
        else:
            # push coordinate space of this shape
            graphics.csstack.push()
            # draw shape onto every link
            for link in self.links:
                link.draw(stage, graphics)
                # revert coordinate space that was altered by the link
                # to equal the coordinate space of this shape
                graphics.csstack.revert()
            # remove the coordinate space of this shape from the stack
            graphics.csstack.pop()
            return False


    def draw_transitional(self, stage, graphics):
        """
        Draw the shape in transition from a line to the full shape
        :param stage: stage
        :param graphics: graphics object to draw onto
        """
        for link in self.links:
            graphics.draw_local(link.vtx1.pos(stage), link.vtx2.pos(stage), stage)

    def set_zeroshape(self, vtx):
        """
        Set zero shape position for each vertex
        """
        vtxamount = len(vtx)
        dx = self.length/(vtxamount-1)
        for i in range(vtxamount):
            vtx[i].set_zeropos(i*dx, 0)
