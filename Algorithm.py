import copy

from typing import List

from Board import Board
from Open import OpenHeap
from Node import Node


class Algorithm:
    def __init__(self):
        self._open = OpenHeap()  # also includes the f-score
        self._closed = set()
        self._successor = {}
        self._g = {}
        self._nodes = {}

    def h(self, node) -> int:
        """

        """

        pass

    def g(self, node_key) -> int:
        """
        Cost of the shortest path to node

        """

        return self._g.get(node_key)

    def f(self, node):
        """
        Custom cost function

        """

        return self.g(node) + self.h(node)

    def run(self, starting_board: Board):
        """
        Run the A star algorithm

        Args:
            starting_board(Board): The starting board.

        """

        starting_board_key = starting_board.generateKey()
        self._nodes[starting_board_key] = starting_board

        # initialize start node

        # put start_node in openlist and calculate f = g(s) + h(s) = 0 + h(s)
        self._open.push(node=starting_board_key, f=0)

        # set g_score
        self._g[starting_board_key] = 0

        while self._open.isNotEmpty():
            # choose node from _open with minimal f(x)
            minimal_f, minimal_node = self._open.pop_smallest()

            # and put it to _closed
            self._closed.add(minimal_node)
            # todo: Maybe delete node from "nodes" to save memory

            # check for solution --> player on top right tile and tile _open on top
            if self._nodes.get(minimal_node).did_player_win():
                return  # todo:  return correct path

            # loop through all children of node with minimal f
            for expanded_node, expanded_node_key in self.expand_node(self._nodes.get(minimal_node)):

                # Only process node if it is not already in closed
                if expanded_node_key not in self._closed:
                    g = self.g(minimal_node) + 1  # todo: adjust maybe

                    # check if expanded node is in open
                    node_in_open = self._open.contains(expanded_node_key)

                    # Only process node if it is not in OPEN or it has a smaller g value than existing node
                    if not node_in_open or g < self.g(expanded_node_key):
                        # set successor of expanded node to minimal_node
                        self._successor[expanded_node_key] = minimal_node

                        # set g and f
                        self._g[expanded_node_key] = g
                        f = g + self.h(expanded_node_key)  # todo: Adjust h --> pass actual node

                        # replace f value for the node, else push expanded node
                        if node_in_open:
                            self._open.replace(expanded_node_key, f)
                        else:
                            self._open.push(expanded_node_key, f)

                            # Save the node/board of the expanded key
                            self._nodes[expanded_node_key] = expanded_node

        print("No solution found!")

    def expand_node(self, node, debug=False):

        """
        Expands a node, and returns all possible nodes (moves that could be played)
        This can either be a movement of the player or a movement of the board.

        Args:
            node(Board) : The Node that should be expanded

        Returns:
            tuple[Board, str]: A Tuple of the generated boards and it´s string encodings.
        """

        initial_board = copy.deepcopy(node)

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

        boards = walkable_boards + permutation_boards

        if debug:
            print(f"______________ walkable boards ______________")
            for board in walkable_boards:
                print(board)

            print("______________ permutation boards ______________")
            for board in permutation_boards:
                print(board)

        # create keys for each board
        return [(board, board.generateKey()) for board in boards]


if __name__ == "__main__":
    board = Board()

    test = Algorithm()

    board.setPlayerPosition(3, 2)
    print("--------- initial board ------------")
    print(board)
    boards = test.expand_node(board)

    print(f"______________ possible boards ______________")
    for board, key in boards:
        print(key)
        print(board)
