from Vertex import Vertex
from Shape import Shape
from Environment import Environment
from Settings import Settings
from math import pi, sqrt

def main():
    d = 100*sqrt(3)/6
    vtx = ((0, 0), (50, d), (50, -d), (100, 0))
    sh = Shape([Vertex(x, y) for x, y in vtx])

    s = Settings('settings.ini')
    e = Environment(sh, s)
    e.runmode()

main()
