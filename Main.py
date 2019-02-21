from Vertex import Vertex
from Shape import Shape
from Environment import Environment
from Settings import Settings
from math import pi, sqrt
from Debugger import Debugger

def main():
    c = sqrt(3) / 2
    vtx = ((0, 0), (50, 50), (100, 0))
    sh = Shape([Vertex(x, y) for x, y in vtx])

    s = Settings('settings.ini')
    d = Debugger(s)
    e = Environment(sh, s, d)
    e.runmode()

main()
