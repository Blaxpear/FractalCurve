from Vertex import Vertex
from Shape import Shape
from Environment import Environment


def main():
    vtx1 = Vertex(0, 0, 0, 0)
    vtx2 = Vertex(10, 0, 10, 0)
    s = Shape([vtx1, vtx2])
    e = Environment(s)
    e.mainloop()




main()
