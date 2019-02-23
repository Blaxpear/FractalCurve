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
                         'link': self.add_link}
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

            for type, function in self.commands.items():
                if rowtype == type:
                    function(columns)
                    break

        if not self.manual_zeropos:
            self.shape.set_zeroshape(self.vertices)
        return self.shape

    def add_vertex(self, columns):
        """
        Read columns and save vertex into self.vertices
        :param columns: columns of the row
        """
        coordinates = columns[1].split(';')
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

    def set_start(self, columns):
        """
        Set the vertex that will be drawn to the origin of the link.
        :param columns: columns of the row
        Columns's second element must be an integer index (starting from 1) of the previously saved vertex
        """
        setting = columns[1].strip().lower()
        if setting == 'first':
            vtx_index = 1
        else:
            vtx_index = int(columns[1])
        self.shape.start = self.vertices[vtx_index - 1]

    def set_end(self, columns):
        """
        Set the vertex that will be drawn to the end of the link and calculate the length of the shape.
        Start vertex must be defined before calling this.
        :param columns: columns of the row
        Columns's second element must be an integer index (starting from 1) of the previously saved vertex.
        """
        setting = columns[1].strip().lower()
        if setting == 'last':
            vtx_index = len(self.vertices)
        else:
            vtx_index = int(columns[1])
        self.shape.end = self.vertices[vtx_index - 1]
        self.shape.length = self.shape.start.distanceTo(self.shape.end)

    def add_link(self, columns):
        """
        Add a link into self.shape
        :param columns: columns of the row
        Columns's second element is a list delimited by ';'
        elements:
        1: index of first vertex (starting from 1)
        2: index of second vertex
        3: 0/1 boolean integer for mirroring x-axis
        4: 0/1 boolean integer for mirroring y-axis
        vertices at those indexes must be defined before calling this
        """
        ind1, ind2, mir_x, mir_y = columns[1].split(';')
        ind1 = int(ind1) - 1
        ind2 = int(ind2) - 1
        mir_x = mir_x.strip() == '1'
        mir_y = mir_y.strip() == '1'
        self.shape.links.append(self.shape.get_link(self.vertices[ind1], self.vertices[ind2], mir_x, mir_y))

