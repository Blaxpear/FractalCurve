from Vertex import Vertex
from Shape import Shape
from Environment import Environment
from Settings import Settings

def main():
    vtx1 = Vertex(0, 0, 0, 0)
    vtx2 = Vertex(25, 25, 75, 0)
    vtx3 = Vertex(75, -25, 75, 0)
    vtx4 = Vertex(100, 0, 100, 0)
    sh = Shape([vtx1, vtx2, vtx3, vtx4])

    s = Settings('settings.ini')
    e = Environment(sh, s)
    e.mainloop()




main()
