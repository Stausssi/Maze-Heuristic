class Algorithm:
    def __init__(self):
        self.open = []
        self.closed = []
        self.path = []

    def h(self, node) -> int:
        """

        """

        pass

    def g(self, node) -> int:
        """
        Cost of the shortest path to node

        """

        pass

    def f(self, node):
        """
        Custom cost function

        """

        return self.g(node) + self.h(node)

    def run(self, start_node):
        """
        Run the A star algorithm

        """

        # initialize

        # g(start_node) = 0
        # open = [start_node]
        # Path(start_node) = start_node
        # calculate h(start_node)
        # calculate f(start_node) = g(start_node) + h(start_node)

        while self.open:
            # choose node from open with minimal f(x)
            min_index = self.open.index(min([self.f(node) for node in self.open]))
            # remove node from open
            min_node = self.open.pop(min_index)
            # and put it to closed
            self.closed.append(min_node)

            # check for solution

            # expand node

        print("No solution found!")

