import copy


class CSStack:
    """
    Coordinate space stack. Uses a reference to a coordinate space to create deep copies of it into a stack
    """
    def __init__(self, coordinatespace):
        """
        Initialize coordinate space stack
        :param coordinatespace: reference to the coordinate space object
        """
        self.local = coordinatespace
        self.stack = []

    def push(self):
        """
        Push the current coordinate space into the stack
        """
        self.stack.append(copy.deepcopy(self.local))

    def revert(self):
        """
        Save coordinate space from stack into current coordinate space
        """
        self.local.make_equal(self.stack[-1])

    def pop(self):
        """
        Pop the last coordinate space in stack
        :return: Coordinatespace
        """
        return self.stack.pop()
