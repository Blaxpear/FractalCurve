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
        self.links = []
        # list of Vertex object pairs to only draw lines
        self.visuals = []

    def link(self, vtx1, vtx2, mirror_y):
        """
        Save a link between these vertices
        :param vtx1: first vertex
        :param vtx2: second vertex
        :param mirror_y: boolean
        """
        d = vtx1.distanceTo(vtx2)
        scale = d / self.length
        self.links.append(Link(vtx1, vtx2, scale, self, mirror_y=mirror_y))

    def add_visual(self, vtx1, vtx2):
        """
        Save a visual line between these lines
        :param vtx1: first vertex
        :param vtx2: second vertex
        """
        self.visuals.append((vtx1, vtx2))

    def draw(self, stage, graphics) -> bool:
        """
        Draw shape in given stage
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
            self.draw_visuals(stage, graphics)
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
        self.draw_visuals(stage, graphics)

    def draw_visuals(self, stage, graphics):
        """
        Draw visual lines
        :param stage: stage
        :param graphics: graphics object to draw onto
        :return:
        """
        clamped_stage = min(stage, 1)
        stage_remainder = stage % 1
        for visual in self.visuals:
            graphics.draw_local(visual[0].pos(clamped_stage), visual[1].pos(clamped_stage), stage_remainder)

    def set_zeroshape(self, vtx):
        """
        Set zero shape position for each vertex
        """
        vtxamount = len(vtx)
        dx = self.length/(vtxamount-1)
        for i in range(vtxamount):
            vtx[i].set_zeropos(i*dx, 0)
