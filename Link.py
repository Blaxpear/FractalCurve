
class Link:
    """
    Single connection between two of the shape's vertices
    """
    def __init__(self, vtx1, vtx2, scale):
        self.vtx1 = vtx1
        self.vtx2 = vtx2
        self.angle = vtx1.angleTo(vtx2)
        self.scale = scale
