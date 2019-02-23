from Shape import Shape
from Vertex import Vertex

class ShapeFileHandler:
    """
    Class for loading and saving Shape objects
    """
    def __init__(self):
        self.commands = {'vertex': self.add_vertex,
                         'start': self.set_start,
                         'end': self.set_end,
                         'link': self.add_link,
                         'link all': self.link_all}
        self.vertices = None
        self.shape = None
        self.manual_zeropos = False

    def load(self, path) -> Shape:
        """
        Load a Shape object from path
        :param path: path to shape file
        :return: Shape object
        """
        f = open(path, "r")
        self.vertices = []
        self.shape = Shape()
        self.manual_zeropos = False
        for line in f.readlines():

            columns = line.split(':')
            rowtype = columns[0]
            arguments = columns[1]
            for type, function in self.commands.items():
                if rowtype == type:
                    function(arguments)
                    break

        if not self.manual_zeropos:
            self.shape.set_zeroshape(self.vertices)
        return self.shape

    def add_vertex(self, arguments):
        """
        Save vertex into self.vertices
        :param arguments:
        string that contains: "x, y; x0, y0"
        x, y are full stage position. required
        x0, y0 are zero stage position. optional, if omitted no semicolon should follow y argument
        """
        coordinates = arguments.split(';')
        if not self.manual_zeropos and len(coordinates) == 2:
            # two coordinates given, so zero positions are manually set
            self.manual_zeropos = True

        if self.manual_zeropos:
            # on each vertex row there are two xy pairs
            fullstage, zerostage = coordinates
            x, y = fullstage.split(',')
            x0, y0 = zerostage.split(',')
            vtx = Vertex(float(x), float(y))
            vtx.set_zeropos(float(x0), float(y0))
            self.vertices.append(vtx)
        else:
            # on each vertex row there are only one xy pair
            # zero positions will be distributed equally along a
            # line from start vertex to end vertex
            x, y = coordinates[0].split(',')
            self.vertices.append(Vertex(float(x), float(y)))

    def set_start(self, index):
        """
        Set the vertex that will be drawn to the origin of the link.
        :param index:
        A string containing integer index (starting from 1) referring to previously saved vertex
        """
        setting = index.strip().lower()
        if setting == 'first':
            vtx_index = 1
        else:
            vtx_index = int(index)
        self.shape.start = self.vertices[vtx_index - 1]

    def set_end(self, index):
        """
        Set the vertex that will be drawn to the end of the link and calculate the length of the shape.
        Start vertex must be defined before calling this.
        :param index:
        A string containing integer index (starting from 1) referring to previously saved vertex
        """
        setting = index.strip().lower()
        if setting == 'last':
            vtx_index = len(self.vertices)
        else:
            vtx_index = int(index)
        self.shape.end = self.vertices[vtx_index - 1]
        self.shape.length = self.shape.start.distanceTo(self.shape.end)

    def add_link(self, arguments):
        """
        Add a link into self.shape
        :param arguments:
        A string that has elements delimited by ';'
        elements:
        1: index of first vertex (starting from 1)
        2: index of second vertex
        3: 0/1 boolean integer for mirroring x-axis
        4: 0/1 boolean integer for mirroring y-axis
        vertices at those indexes must be defined before calling this
        """
        ind1, ind2, mir_x, mir_y = arguments.split(';')
        ind1 = int(ind1) - 1
        ind2 = int(ind2) - 1
        mir_x = mir_x.strip() == '1'
        mir_y = mir_y.strip() == '1'
        self.shape.links.append(self.shape.get_link(self.vertices[ind1], self.vertices[ind2], mir_x, mir_y))

    def link_all(self, arguments):
        """
        Link all vertices in the order they were saved
        :param arguments:
        A string that has elements delimited by ';'
        elements:
        1: 0/1 boolean integer for y-mirroring all odd links
        2: 0/1 boolean integer for y-mirroring all even links
        """
        mir_y_odd = arguments.split(';')[0].strip() == '1'
        mir_y_even = arguments.split(';')[1].strip() == '1'
        for i in range(len(self.vertices) - 1):
            if i % 2 == 0:
                self.shape.link(self.vertices[i], self.vertices[i + 1], mirror_y=mir_y_even, mirror_x=False)
            else:
                self.shape.link(self.vertices[i], self.vertices[i + 1], mirror_y=mir_y_odd, mirror_x=False)
