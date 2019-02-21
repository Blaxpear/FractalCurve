from copy import deepcopy


class TopLink:
    """
    Class for storing an object behaving like a link that draws the
    last shape at some certain stage. This can be used to optimize
    recursion, because top links change only when stage passes whole
    numbers.

    If you calculate a list of top links (the links that draw the last
    shape) every time the stage passes a whole number, you can then
    use the list of top links to draw the shapes, instead of recursively
    calculating each last link during every frame.
    """
    def __init__(self, shape, coordinatespace, debugger):
        """
        :param shape: shape that this link will draw
        :param coordinatespace:
        coordinate space that the shape will be drawn
        on relative to the very first coordinate space
        of the root shape
        :param debugger: reference to Debugger object
        """
        self.debug = debugger
        self.shape = shape
        self.coordinatespace = deepcopy(coordinatespace)

    def draw(self, stage, graphics):
        """
        Change graphics' coordinate space equal to the coordinate
        space of this toplink and draw shape in given stage
        :param stage: stage
        :param graphics: graphics object to draw onto
        """
        # this is the last link so only draw the shape
        # according to the decimal places
        if stage % 1 > 0:
            stage = stage % 1
        else:
            # if remainder is zero, draw full stage
            stage = 1
        graphics.cs.make_equal(self.coordinatespace)
        self.debug.toplink(self.shape.length)
        self.shape.draw(stage, graphics)