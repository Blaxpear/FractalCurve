from Vertex import Vertex
from ShapeFileHandler import ShapeFileHandler
from Environment import Environment
from Settings import Settings
from math import pi, sqrt
from Debugger import Debugger

def main():
    fh = ShapeFileHandler()
    s = Settings('settings.ini')
    sh = fh.load(s.getitem("Program", "shape", str))
    d = Debugger(s)
    e = Environment(sh, s, d)
    e.runmode()

main()
