from Board import Board


class Node:
    def __init__(self, board):

        # board configuration
        self._board = board
        self._successor = None
        self._g = 0

    def g(self):
        return self._g

    def setSuccessor(self, node):
        self._successor = node

    def getBoard(self) -> Board:
        return self._board

