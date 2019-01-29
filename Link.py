
class Link:
    """
    Single connection between two of the shape's vertices
    """
    def __init__(self, vtx1, vtx2, scale, shape):
        self.vtx1 = vtx1
        self.vtx2 = vtx2
        self.angle = vtx1.angleTo(vtx2)
        self.scale = scale
        self.shape = shape

    def draw(self, stage, graphics):
        graphics.cs.set_origin(self.vtx1.pos(stage+1))
        graphics.cs.rotate(self.angle)
        graphics.cs.scale(self.scale)
        self.shape.draw(stage, graphics)
        graphics.csstack.pop()
        graphics.csstack.revert()

