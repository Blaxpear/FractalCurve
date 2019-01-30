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

    s = Settings()
    s.gradient=[[0, 0, 255], [0, 0, 255]]
    s.gradientbounds = 1
    s.resolution = (512, 512)
    s.origin = (256, 256)
    s.scale = 2
    s.angle = 0

    e = Environment(sh, s)
    e.mainloop()




main()
