from Vertex import Vertex
from Shape import Shape
from Environment import Environment
from Settings import Settings
from math import pi, sqrt

def main():
    c = sqrt(3) / 2
    vtx = ((0, 0), (0, 100*c), (0, -10), (100, 0))
    sh = Shape([Vertex(x, y) for x, y in vtx])

    s = Settings('settings.ini')
    e = Environment(sh, s)
    e.runmode()

main()
