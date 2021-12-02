from decimal import getcontext
from multiprocessing import Pool
from statistics import stdev

from scipy.spatial import distance

from Board import Board
from util import BoardHelper

getcontext().prec = 2 * 1000


class Heuristics:
    """
    Static class containing methods for different heuristics.
    """

    @staticmethod
    def euclid_int(player_pos, end_tile_pos):
        """
        Calculates the euclidean distance between two given positions and floors it.

        Args:
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.

        Returns:
            int: The euclidean distance
        """

        return int(distance.euclidean(player_pos, end_tile_pos))

    @staticmethod
    def euclid(player_pos, end_tile_pos):
        """
        Calculates the euclidean distance between two given positions.

        Args:
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.

        Returns:
            float: The euclidean distance
        """

        return distance.euclidean(player_pos, end_tile_pos)

    @staticmethod
    def manhattan(player_pos, end_tile_pos):
        """
        Calculates the manhattan distance between two given positions.

        Args:
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.

        Returns:
            int: The manhattan distance
        """

        return int(distance.cityblock(player_pos, end_tile_pos))

    @staticmethod
    def minkowski_int(player_pos, end_tile_pos, norm):
        """
        Calculates the minkowski distance between two given positions and floors it.

        Args:
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.
            norm (int): The norm of the minkowski distance. 1 = manhattan, 2 = euclidean

        Returns:
            int: The floored minkowski distance
        """

        return int(distance.minkowski(player_pos, end_tile_pos, p=norm))

    @staticmethod
    def minkowski(player_pos, end_tile_pos, norm):
        """
        Calculates the minkowski distance between two given positions.

        Args:
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.
            norm (int): The norm of the minkowski distance. 1 = manhattan, 2 = euclidean

        Returns:
            float: The minkowski distance
        """

        return distance.minkowski(player_pos, end_tile_pos, p=norm)

    @staticmethod
    def chebyshev(player_pos, end_tile_pos):
        """
        Calculates the chebyshev distance between two given positions.

        Args:
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.

        Returns:
            int: The chebyshev distance
        """

        return distance.chebyshev(player_pos, end_tile_pos)

    @staticmethod
    def min_distance_product(list1, list2):
        """

        Args:
            list1:
            list2:

        Returns:

        """

        list1 = list(list1)
        list2 = list(list2)

        distances = []

        for point1 in list1:
            for point2 in list2:
                distances.append(Heuristics.euclid(point1, point2))

        return min(distances)

    @staticmethod
    def shortest_distance_end_path_player_path(node, player_pos, end_tile_pos, isInt=True):
        """

        Args:
            node:
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.

        Returns:

        """

        player_row, player_column = player_pos
        endTile_row, endTile_column = end_tile_pos

        end_positions = node.get_reachable_positions(endTile_row, endTile_column)
        end_positions.add((endTile_row, endTile_column))

        player_positions = node.get_reachable_positions(player_row, player_column)
        player_positions.add((player_row, player_column))

        if isInt:
            return int(Heuristics.min_distance_product(end_positions, player_positions))
        else:
            return Heuristics.min_distance_product(end_positions, player_positions)

    @staticmethod
    def min_shortest_distance_and_euclid(node, player_pos, end_tile_pos):
        """
        Combines the shortest distance with euclid and chooses the minimum of both metrics.

        Args:
            node (Board): The current board node.
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.

        Returns:
            float: The minimum of both metrics.
        """

        return min(
            Heuristics.euclid_int(player_pos, end_tile_pos),
            Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos)
        )

    @staticmethod
    def sum_shortest_distance_and_euclid_int(node, player_pos, end_tile_pos, weight_euclid=1, weight_path=1):
        """
        Combines the shortest distance with euclid by adding them together and flooring the product.

        Args:
            node (Board): The current board node.
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.
            weight_euclid (float): The weight of the euclidean distance.
            weight_path (float): The weight of the shortest distance to the end path.

        Returns:
            int: The weighted product of euclid and shortest distance
        """

        return int(
            Heuristics.euclid(player_pos, end_tile_pos) * weight_euclid +
            Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos, isInt=False) * weight_path
        )

    @staticmethod
    def sum_shortest_distance_and_euclid(node, player_pos, end_tile_pos, weight_euclid=1, weight_path=1):
        """
        Combines the shortest distance with euclid by adding them together.

        Args:
            node (Board): The current board node.
            player_pos (tuple[int, int]): The position of the player.
            end_tile_pos (tuple[int, int]): The position of the end tile.
            weight_euclid (float): The weight of the euclidean distance.
            weight_path (float): The weight of the shortest distance to the end path.

        Returns:
            float: The weighted product of euclid and shortest distance
        """

        return \
            Heuristics.euclid(player_pos, end_tile_pos) * weight_euclid + \
            Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos, isInt=False) * weight_path

    @staticmethod
    def harmonic_mean(node, player_pos, end_tile_pos):

        player_row, player_column = player_pos
        endTile_row, endTile_column = end_tile_pos

        end_positions = node.get_reachable_positions(endTile_row, endTile_column)
        end_positions.add((endTile_row, endTile_column))

        player_positions = node.get_reachable_positions(player_row, player_column)
        player_positions.add((player_row, player_column))

        min_dist = Heuristics.min_distance_product(end_positions, player_positions)
        player_to_end = Heuristics.euclid(end_positions, player_positions)

        try:
            return (min_dist * player_to_end) / (min_dist + player_to_end)
        except ZeroDivisionError:
            return 0


def threadPoolCalc(boards, heuristic):
    """
    Calculates the given boards with the given heuristic in a thread pool.

    Args:
        boards (list[Board]): A list of boards to calculate
        heuristic (str): The identifier of the heuristic

    Returns:
        list: The list of paths and openCounts for every board
    """

    params = [(board, heuristic) for board in boards]

    with Pool(len(boards)) as threadPool:
        return threadPool.map(evaluateBoard, params)


def evaluateBoard(param):
    """
    Evaluates a board.

    Args:
        param (tuple[Board, str]): A tuple containing the board and heuristic

    Returns:
        tuple: The path and open count of the solved board.
    """

    board, heuristic = param
    print(board)
    # print(board)
    from Algorithm import Algorithm
    alg = Algorithm(heuristic)
    path = alg.run(board)
    # print("Done with a board!")
    return path


def evaluate():
    """
    Evaluates many boards with many heuristics.

    Returns:
        None: Nothing
    """

    board_count = 30

    # Create a list containing the heuristics
    heuristics = [
        "minkowski", "minkowski_int",
        "euclid", "euclid_int",
        "manhattan",
        "chebyshev",
        "shortest_distance", "shortest_distance_int",
        "min_shortest_distance",
        "sum_shortest_distance",
    ]

    # Add weighted heuristics
    for i in range(1, 10):
        float_i = i / 10
        float_j = 1 - float_i
        heuristics.append(f"sum_shortest_distance_{float_i}_{float_j}")
    for i in range(1, 10):
        float_i = i / 10
        float_j = 1 - float_i
        heuristics.append(f"sum_shortest_distance_int_{float_i}_{float_j}")
    # Evaluate 30 Boards in total
    # First, the two given boards
    # Then 28 random
    boards = []
    for boardIndex in range(1, 3):
        field, spareTile = BoardHelper.readBoardFromCSV(f"data/puzzle_{boardIndex}.csv")
        startColumn, endColumn = BoardHelper.readBoardInformation(f"data/info_{boardIndex}.txt")
        board = BoardHelper.generateBoard(field, spareTile, startColumn, endColumn)

        boards.append(board)

    for _ in range(board_count - 2):
        board = Board()
        board.initRandom()
        boards.append(board)

    allMoves = []
    allOpen = []
    for heuristic in heuristics:
        print(f"Calculating with {heuristic}...")
        paths = threadPoolCalc(boards, heuristic)

        # print(f"---------- [{heuristic}] ----------")
        moves = []
        openCount = []
        removeCount = 0
        for index, path in enumerate(paths):
            if path[1] > 0:
                moves.append(len(path[0]))
                openCount.append(path[1])
            else:
                print(f"{heuristic} failed with Board {index - removeCount}!")
                # Remove board from boards
                boards.pop(index - removeCount)

                # Remove previous entries of the board with previous heuristics
                for prevMoves in allMoves:
                    prevMoves.pop(index - removeCount)
                for prevOpenCounts in allOpen:
                    prevOpenCounts.pop(index - removeCount)

                removeCount += 1

        allMoves.append(moves)
        allOpen.append(openCount)
        print(f"{heuristic} done!")

    # This dict will contain the average values for every heuristic
    heuristics_values = {}

    # Go over every value and calculate the averages
    for heuristic, moves, openCount in zip(heuristics, allMoves, allOpen):
        avgMoves = sum(moves) / len(moves)
        stdMoves = stdev(moves)
        avgOpen = sum(openCount) / len(openCount)
        stdOpen = stdev(openCount)

        heuristics_values.update({
            heuristic: (avgMoves, stdMoves, avgOpen, stdOpen)
        })

    print(heuristics_values)


if __name__ == "__main__":
    evaluate()
