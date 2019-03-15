
class Link:
    """
    Single connection between two of the shape's vertices
    """
    def __init__(self, vtx1, vtx2, scale, shape, mirror_y):
        self.vtx1 = vtx1
        self.vtx2 = vtx2
        self.angle = vtx1.angleTo(vtx2)
        self.scale = scale
        self.shape = shape
        self.mirror_y = mirror_y

    def draw(self, stage, graphics):

        graphics.cs.set_origin(self.vtx1.pos(stage))
        graphics.cs.rotate(self.angle)
        graphics.cs.scale_by(self.scale)

        next_stage = stage - 1

        if self.mirror_y:
            graphics.cs.scale_y(-1)

        self.shape.draw(next_stage, graphics)

