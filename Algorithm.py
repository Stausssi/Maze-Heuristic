import copy
from functools import partial
from typing import List

from Board import Board
from Heuristics import Heuristics
from Open import OpenHeap


class Algorithm:
    def __init__(self, heuristic=None):
        """
        Represents the A* Algorithm.

        Args:
            heuristic (str or None): The optional heuristic to use for the algorithm. If this is None, it will choose
                the defined heuristic.
        """

        self._open = OpenHeap()  # also includes the f-score
        self._closed = set()
        self._predecessor = {}
        self._g = {}
        self._nodes = {}
        self.heuristic = heuristic

    def h(self, node):
        """
        Calculates the heuristic for the algorithm. It is possible, to select many different heuristics for evaluation.s
        The standard heuristic is Heuristics.sum_shortest_distance_and_euclid with weighs 0.4 and 0.6.

        Args:
            node (Board): The graph node containing board information

        Returns:
            float: The heuristic value.
        """

        player_pos = node.getPlayerPosition()
        end_tile_pos = node.getEndTilePosition()

        if self.heuristic is None:
            return Heuristics.sum_shortest_distance_and_euclid(node, player_pos, end_tile_pos, 0.4, 0.6)
        else:
            # Create partial methods for every heuristic
            heuristics = {
                "euclid": partial(Heuristics.euclid, player_pos, end_tile_pos),
                "euclid_int": partial(Heuristics.euclid_int, player_pos, end_tile_pos),
                "manhattan": partial(Heuristics.manhattan, player_pos, end_tile_pos),
                "minkowski": partial(Heuristics.minkowski, player_pos, end_tile_pos, 3),
                "minkowski_int": partial(Heuristics.minkowski_int, player_pos, end_tile_pos, 3),
                "chebyshev": partial(Heuristics.chebyshev, player_pos, end_tile_pos),
                "min_distance": partial(
                    Heuristics.min_distance_product,
                    node.get_reachable_positions(*player_pos),
                    node.get_reachable_positions(*end_tile_pos)
                ),
                "shortest_distance": partial(
                    Heuristics.shortest_distance_end_path_player_path, node, player_pos, end_tile_pos, False
                ),
                "shortest_distance_int": partial(
                    Heuristics.shortest_distance_end_path_player_path, node, player_pos, end_tile_pos
                ),
                "min_shortest_distance": partial(
                    Heuristics.min_shortest_distance_and_euclid, node, player_pos, end_tile_pos
                ),
                "sum_shortest_distance": partial(
                    Heuristics.sum_shortest_distance_and_euclid, node, player_pos, end_tile_pos
                )
            }

            # Weighted heuristics
            for i in range(1, 10):
                float_i = i / 10
                float_j = 1 - float_i
                heuristics.update({
                    f"sum_shortest_distance_{float_i}_{float_j}": partial(
                        Heuristics.sum_shortest_distance_and_euclid, node, player_pos, end_tile_pos, float_i, float_j
                    )
                })

            for i in range(1, 10):
                float_i = i / 10
                float_j = 1 - float_i
                heuristics.update({
                    f"sum_shortest_distance_int_{float_i}_{float_j}": partial(
                        Heuristics.sum_shortest_distance_and_euclid_int, node, player_pos, end_tile_pos, float_i, float_j
                    )
                })

            return heuristics.get(self.heuristic)()

    def g(self, node_key) -> int:
        """
        Returns the cost of the shortest path to the current node.

        Args:
            node_key: The key to the node

        Returns:
            int: The costs to the current node.
        """

        return self._g.get(node_key)

    def f(self, node):
        """
        Combines g(x) and h(x).

        Args:
            node (Board): The node to calculate the metric of

        Returns:
            int: The metric.
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
        predecessor_key = node_key

        while predecessor_key is not None:
            predecessor_key = self._predecessor[predecessor_key]
            moves.insert(0, self._nodes.get(predecessor_key))

        return moves

    def run(self, starting_board: Board):
        """
        Run the A star algorithm

        Args:
            starting_board(Board): The starting board.

        Returns:
            tuple[XX, int]: A tuple containing the path and count of open nodes.
        """

        # initialize start node
        starting_board_key = starting_board.generateKey()
        self._nodes[starting_board_key] = starting_board
        # put start_node in open_heap and calculate f = g(s) + h(s) = 0 + h(s)
        self._open.push(node=starting_board_key, f=0)
        # set g_score
        self._g[starting_board_key] = 0
        # set predecessors
        self._predecessor[starting_board_key] = None

        while self._open.isNotEmpty():
            # choose node from _open with minimal f(x)
            minimal_f, best_node = self._open.pop()
            # and put it to _closed
            self._closed.add(best_node)

            # Stop after 25k open, this is just for benchmarking
            if self._open.size() >= 25_000:
                # print("This param seems unsolvable")
                return [], -1

            # check for solution --> player on top right tile and tile _open on top
            if self._nodes.get(best_node).didPlayerWin():
                # return path and the size of the open_heap
                return self.reconstruct_path(best_node), self._open.size()

            # loop through all children of node with minimal f
            for child_node, child_node_key in self.expand_node(self._nodes.get(best_node)):

                # Only process node if it is not already in closed
                if child_node_key not in self._closed:

                    # calculate the g value of the new node
                    g = self.g(best_node) + 1

                    # check if child node is in open
                    node_in_open = self._open.contains(child_node_key)

                    # Only process node if it is not in OPEN or it has a smaller g value than existing node
                    if not node_in_open or g < self.g(child_node_key):
                        # set predecessor of child node to best_node
                        self._predecessor[child_node_key] = best_node

                        # set g and f
                        self._g[child_node_key] = g
                        f = g + self.h(child_node)

                        # replace f value for the node, else push child node to open
                        if node_in_open:
                            self._open.replace(child_node_key, f)
                        else:
                            self._open.push(child_node_key, f)

                            # Save the node/param of the child key
                            self._nodes[child_node_key] = child_node

    @staticmethod
    def expand_node(node, debug=False):
        """
        Expands a node, and returns all possible nodes (moves that could be played)
        This can either be a movement of the player or a movement of the param.

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

        # generate all permutations of the param by pushing a tile in
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

        # create keys for each param
        return [(board, board.generateKey()) for board in boards]


if __name__ == "__main__":
    board = Board()

    test = Algorithm()

    board.setPlayerPosition(1, 4)
    print("--------- initial param ------------")
    print(board)
    boards = test.expand_node(board)

    print(f"______________ possible boards ______________")
    for board, key in boards:
        print(key)
        print(board)
