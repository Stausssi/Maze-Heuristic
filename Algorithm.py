from Board import Board
from Open import OpenHeap
from Node import Node


class Algorithm:
    def __init__(self, board):
        # optimize with dictionairy
        self._open = OpenHeap()
        self._closed = set()
        self._path = {}
        self._g = {}

        self._board = board

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

    def run(self, board):
        """
        Run the A star algorithm

        """

        # initialize start node
        start_node = Node(board=board, g=0)
        start_node.setSuccessor(None)

        # put start_node in openlist and calculate f = g(s) + h(s) = 0 + h(s)
        self._open.push(node=start_node, f=0)

        # add node to path
        self._path[start_node] = [start_node]

        while self._open.isNotEmpty():
            # choose node from _open with minimal f(x)
            best_node = self._open.pop_smallest()

            # and put it to _closed
            self._closed.add(best_node)

            # check for solution --> player on top right tile and tile _open on top
            if self._board.did_player_win():
                return self._path  # return correct path

            # get costs (g) of minimal node

            # expand node with minimal f
            for expanded_node in self.expand_node(best_node):

                # Only process node if it is not already in closed
                if expanded_node not in self._closed:
                    g = self.g(best_node) + 1  # todo: adjust

                    # Only process node if it is not in OPEN or it has a smaller g value # todo: than what ? 
                    if not self._open.contains(expanded_node) or g < self.g(expanded_node):

                        # set successor of expanded node to best_node
                        expanded_node.setSuccessor(best_node)

                        expanded_node._g = g
                        f = g + self.h(expanded_node)

                        # replace f value for the node, else push expanded node
                        self._open.replace_or_push(expanded_node, f)

        print("No solution found!")

    def append_path(self, previous_node, new_node):
        """

        Args:
            previous_node:
            new_node:

        Returns:

        """
        self._path.get(previous_node)
        self._path[new_node].append(new_node)

    def expand_node(self, node) -> [Board]:

        """
        Expands a node, and returns all possible node (moves that could be played)
        """

        return []

    def get_reachable_tiles(self):
        """

        :return:
        """

        pass
