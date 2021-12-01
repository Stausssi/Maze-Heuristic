import copy

from typing import List

from Board import Board
from Open import OpenHeap
from Heuristics import Heuristics


class Algorithm:
    def __init__(self):
        self._open = OpenHeap()  # also includes the f-score
        self._closed = set()
        self._successor = {}
        self._g = {}
        self._nodes = {}

    def h(self, node):
        """
        Args:
            node (Board):

        """

        player_pos = node.getPlayerPosition()
        end_tile_pos = node.getEndTile()

        # return Heuristics.euclid(player_pos, end_tile_pos)
        # return Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos)
        # return Heuristics.manhattan(player_pos, end_tile_pos)
        # return Heuristics.minkowski(player_pos, end_tile_pos, 2)
        # return Heuristics.minkowski(player_pos, end_tile_pos, 3)
        return Heuristics.chebyshev(player_pos, end_tile_pos)

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

    def reconstruct_path(self, node_key):
        """
        Return the path (list of Boards) that resulted in the current node_key.

        Args:
            node_key (str): Key of the node whose path should be reconstructed

        Returns:
            list[Board]: Moves that led to the current node

        """

        moves = [self._nodes[node_key]]
        successor_key = node_key

        while successor_key is not None:
            successor_key = self._successor[successor_key]
            moves.insert(0, self._nodes.get(successor_key))

        return moves

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
        self._open.push(node=starting_board_key, f=self.h(starting_board))

        # set g_score
        self._g[starting_board_key] = 0

        # set successors
        self._successor[starting_board_key] = None

        while self._open.isNotEmpty():
            # Logging
            print(f"Open: {self._open.size()}, Closed: {len(self._closed)}")

            # choose node from _open with minimal f(x)
            minimal_f, minimal_node = self._open.pop_smallest()

            # and put it to _closed
            self._closed.add(minimal_node)
            # todo: Maybe delete node from "nodes" to save memory

            # check for solution --> player on top right tile and tile _open on top
            if self._nodes.get(minimal_node).did_player_win():
                # return path
                return self.reconstruct_path(minimal_node)

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
                        f = g + self.h(expanded_node)

                        # replace f value for the node, else push expanded node
                        if node_in_open:
                            self._open.replace(expanded_node_key, f)
                        else:
                            self._open.push(expanded_node_key, f)

                            # Save the node/board of the expanded key
                            self._nodes[expanded_node_key] = expanded_node

    @staticmethod
    def expand_node(node, debug=False):

        """
        Expands a node, and returns all possible nodes (moves that could be played)
        This can either be a movement of the player or a movement of the board.

        Args:
            node(Board) : The Node that should be expanded
            debug (bool): True if the resulting boards should be printed

        Returns:
            tuple[Board, str]: A Tuple of the generated boards and it´s string encodings.
        """

        initial_board = copy.deepcopy(node)

        # calculate positions, the player could move to
        player_row, player_col = initial_board.getPlayerPosition()
        player_positions = initial_board.get_reachable_positions(player_row, player_col)

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

    board.setPlayerPosition(1, 4)
    print("--------- initial board ------------")
    print(board)
    boards = test.expand_node(board)

    print(f"______________ possible boards ______________")
    for board, key in boards:
        print(key)
        print(board)
