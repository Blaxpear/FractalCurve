from Vertex import Vertex
from Shape import Shape
from Graphics import Graphics


def main():
    vtx1 = Vertex(0, 0, 0, 0)
    vtx2 = Vertex(10, 0, 10, 0)
    s = Shape([vtx1, vtx2])
    g = Graphics(s)
    while True:
        g.updatescreen(0)




main()
