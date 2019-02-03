from Vertex import Vertex
from Shape import Shape
from Environment import Environment
from Settings import Settings

def main():
    vtx1 = Vertex(0, 0, 0, 0)
    vtx2 = Vertex(50, -20, 50, 0)
    vtx4 = Vertex(100, 0, 100, 0)
    sh = Shape([vtx1, vtx2, vtx4])

    s = Settings('settings.ini')
    e = Environment(sh, s)
    e.runmode()




main()
