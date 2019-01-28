from Vertex import Vertex
from Shape import Shape
from Environment import Environment


def main():
    vtx1 = Vertex(0, 0, 0, 0)
    vtx2 = Vertex(25, 10, 25, 0)
    vtx3 = Vertex(50, 0, 50, 0)
    s = Shape([vtx1, vtx2, vtx3])
    e = Environment(s)
    e.mainloop()




main()
