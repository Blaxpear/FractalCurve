from Vertex import Vertex
from ShapeFileHandler import ShapeFileHandler
from Environment import Environment
from Settings import Settings
from math import pi, sqrt
from Debugger import Debugger

def main():
    fh = ShapeFileHandler()
    sh = fh.load('test.shape')
    s = Settings('settings.ini')
    d = Debugger(s)
    e = Environment(sh, s, d)
    e.runmode()

main()
