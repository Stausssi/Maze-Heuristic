import copy

from typing import List

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
        start_node = Node(board=board)
        start_node.setSuccessor(None)

        # put start_node in openlist and calculate f = g(s) + h(s) = 0 + h(s)
        self._open.push(node=start_node, f=0)

        # add node to path
        self._path[start_node] = [start_node]

        while self._open.isNotEmpty():
            # choose node from _open with minimal f(x)
            minimal_node = self._open.pop_smallest()

            # and put it to _closed
            self._closed.add(minimal_node)

            # check for solution --> player on top right tile and tile _open on top
            if self._board.did_player_win():
                return self._path  # return correct path

            # get costs (g) of minimal node

            # expand node with minimal f
            for expanded_node in self.expand_node(minimal_node):

                # Only process node if it is not already in closed
                if expanded_node not in self._closed:
                    g = self.g(minimal_node) + 1  # todo: adjust

                    # Only process node if it is not in OPEN or it has a smaller g value # todo: than what ? 
                    if not self._open.contains(expanded_node) or g < self.g(expanded_node):

                        # set successor of expanded node to minimal_node
                        expanded_node.setSuccessor(minimal_node)

                        expanded_node._g = g
                        f = g + self.h(expanded_node)

                        # replace f value for the node, else push expanded node
                        self._open.replace_or_push(expanded_node, f)

        print("No solution found!")

    def expand_node(self, node) -> [Board]:

        """
        Expands a node, and returns all possible nodes (moves that could be played)
        This can either be a movement of the player or a movement of the board.

        """

        initial_board = copy.deepcopy(node.getBoard())

        # calculate positions, the player could move to
        player_positions = initial_board.get_reachable_positions()

        # generate boards, where the player is at those positions
        walkable_boards: List[Board] = []
        for row, column in player_positions:
            new_board = copy.deepcopy(initial_board)
            new_board.setPlayerPosition(column, row)
            walkable_boards.append(new_board)

        # generate all permutations of the board by pushing a tile in
        permutation_boards: List[Board] = []
        # push the spare tile in at every row
        for row_index in range(initial_board.getSize()[0]):
            new_board = copy.deepcopy(initial_board)
            new_board.pushSpareTileIn(rowIndex=row_index)
            permutation_boards.append(new_board)

        return walkable_boards, permutation_boards


if __name__ == "__main__":
    board = Board()

    test = Algorithm(board)

    board.setPlayerPosition(3, 2)
    print("--------- initial board ------------")
    print(board)
    walkable_boards, permutation_boards = test.expand_node(Node(board))
    print(f"______________ walkable boards ({len(walkable_boards)}) ______________")

    for board in walkable_boards:
        print(board.generateKey())
        print(board)
    print("______________ permutation boards ______________")
    for board in permutation_boards:
        print(board.generateKey())
        print(board)




