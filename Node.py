class Node:
    def __init__(self, board, g):

        # board configuration
        self._board = board
        self._successor = None
        self._g = g

    def g(self):
        return self._g

    def setSuccessor(self, node):
        self._successor = node

