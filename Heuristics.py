from decimal import getcontext
from multiprocessing import Pool
from statistics import stdev

from scipy.spatial import distance

from Board import Board
from util import BoardHelper

getcontext().prec = 2 * 1000


class Heuristics:
    @staticmethod
    def euclid_int(player_pos, end_tile_pos):

        return int(distance.euclidean(player_pos, end_tile_pos))

    @staticmethod
    def euclid(player_pos, end_tile_pos):

        return distance.euclidean(player_pos, end_tile_pos)

    @staticmethod
    def manhattan(player_pos, end_tile_pos):
        return int(distance.cityblock(player_pos, end_tile_pos))

    @staticmethod
    def minkowski_int(player_pos, end_tile_pos, norm):
        return int(distance.minkowski(player_pos, end_tile_pos, p=norm))

    @staticmethod
    def minkowski(player_pos, end_tile_pos, norm):
        return distance.minkowski(player_pos, end_tile_pos, p=norm)

    @staticmethod
    def chebyshev(player_pos, end_tile_pos):
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
            player_pos:
            end_tile_pos:

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
        return min(
            Heuristics.euclid_int(player_pos, end_tile_pos),
            Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos)
        )

    @staticmethod
    def sum_shortest_distance_and_euclid_int(node, player_pos, end_tile_pos, weight_euclid=1, weight_path=1):
        return int(Heuristics.euclid(player_pos, end_tile_pos) * weight_euclid + \
                   Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos, isInt=False) \
                   * weight_path)

    @staticmethod
    def sum_shortest_distance_and_euclid(node, player_pos, end_tile_pos, weight_euclid=1, weight_path=1):
        return Heuristics.euclid(player_pos, end_tile_pos) * weight_euclid + \
                   Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos, isInt=False) \
                   * weight_path

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
    params = [(board, heuristic) for board in boards]

    with Pool(len(boards)) as threadPool:
        return threadPool.map(evaluateBoard, params)


def evaluateBoard(param):
    board, heuristic = param
    print(board)
    # print(board)
    from Algorithm import Algorithm
    alg = Algorithm(heuristic)
    path = alg.run(board)
    # print("Done with a board!")
    return path


def evaluate():
    board_count = 30

    heuristics = [
        "minkowski", "minkowski_int",
        "euclid", "euclid_int",
        "manhattan",
        "chebyshev",
        "shortest_distance", "shortest_distance_int",
        "min_shortest_distance",
        "sum_shortest_distance",
    ]

    for i in range(1, 10):
        float_i = i / 10
        float_j = 1 - float_i
        heuristics.append(f"sum_shortest_distance_{float_i}_{float_j}")
    for i in range(1, 10):
        float_i = i / 10
        float_j = 1 - float_i
        heuristics.append(f"sum_shortest_distance_int_{float_i}_{float_j}")

    heuristics_values = {}
    boards = []

    # Evaluate 20 Boards in total
    # First, the two given boards
    # Then 18 random
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

    print(allMoves)
    print(allOpen)

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
