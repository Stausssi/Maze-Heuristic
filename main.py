from multiprocessing import Pool
from statistics import stdev

import Algorithm
from Algorithm import Algorithm
from Board import Board
from util import BoardHelper


def threadPoolCalc(boards, heuristic):
    params = [(board, heuristic) for board in boards]

    with Pool(len(boards)) as threadPool:
        return threadPool.map(evaluateBoard, params)


def evaluateBoard(param):
    board, heuristic = param
    # print(board)
    alg = Algorithm(heuristic)
    path = alg.run(board)
    # print("Done with a board!")
    return path


def main():
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

    # Remove all boards from the list, if manhattan can't complete them
    paths = threadPoolCalc(boards, "manhattan")
    for i, path in enumerate(paths):
        if path[1] < 0:
            boards.pop(i)

    for heuristic in heuristics:
        print(f"Calculating with {heuristic}...")
        paths = threadPoolCalc(boards, heuristic)

        # print(f"---------- [{heuristic}] ----------")
        moves = []
        openCount = []
        stopped = 0
        for index, path in enumerate(paths):
            if path[1] > 0:
                moves.append(len(path[0]))
                openCount.append(path[1])
            else:
                stopped += 1

            # print(f"Solving Board {index + 1} took {len(path[0])} Moves with {path[1]} open")

        avgMoves = sum(moves) / len(moves)
        stdMoves = stdev(moves)
        avgOpen = sum(openCount) / len(openCount)
        stdOpen = stdev(openCount)

        heuristics_values.update({
            heuristic: (avgMoves, stdMoves, avgOpen, stdOpen, stopped)
        })
        print(f"{heuristic} done!")

    print(heuristics_values)

    # Heuristics.euclid: 1 --> 8 Moves (50k Open) mit distance.euclidean: 9 Moves (2.3k Open)
    # Heuristics.euclid: 2 --> 11 Moves (9k Open) mit distance.euclidean: 11 Moves (9k Open) --> oben falsche Werte (?)

    # Heuristics.shortest_distance_end_path_player_path: 1 --> 8 Moves (11k Open)
    # Heuristics.shortest_distance_end_path_player_path: 2 --> 10 Moves (7k Open)

    # Heuristics.manhattan: 1 --> 9 Moves (600 Open)
    # Heuristics.manhattan: 2 --> 12 Moves (15k Open)

    # Heuristics.minkowski: 1 --> 9 Moves (2.3k Open)
    # Heuristics.minkowski: 2 --> 11 Moves (9k Open)
    # --> identisch zu Euklid -> Norm 2
    # Mit Norm 3:
    # Heuristics.minkowski: 1 --> 9 Moves (4k Open)
    # Heuristics.minkowski: 2 --> 11 Moves (18k Open)

    # Heuristics.chebyshev: 1 --> 9 Moves (2.6k Open)
    # Heuristics.chebyshev: 2 --> 11 Moves (10k Open)

    # Heuristics.min_shortest_distance_and_euclid: 1 --> 8 Moves (11.3k Open)
    # Heuristics.min_shortest_distance_and_euclid: 2 --> 10 Moves (7.5k Open)

    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 9 Moves (700 Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 11 Moves (8.7k Open)
    # With euclid weight 2:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 9 Moves (800 Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 13 Moves (8k Open)
    # With euclid weight 0.5:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (1.8k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 11 Moves (3.5k Open)
    # With path weight 2:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 9 Moves (700 Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 12 Moves (650 Open)
    # With path weight 0.5:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 9 Moves (950 Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 12 Moves (6.3k Open)

    # Without integer rounding
    # With euclid weight 0.4, path weight: 0.6:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (2k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 10 Moves (6.5k Open)
    # With euclid weight 0.3, path weight: 0.7:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (3k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 10 Moves (5.3k Open)
    # With euclid weight 0.5, path weight: 0.5:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (1.7k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 10 Moves (6.2k Open)
    # With euclid weight 0.6, path weight: 0.4:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (1.6k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 10 Moves (10k Open)

    # With integer rounding
    # With euclid weight 0.4, path weight: 0.6:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (7k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 10 Moves (6.7k Open)
    # With euclid weight 0.3, path weight: 0.7:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (10k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 10 Moves (7.2k Open)
    # With euclid weight 0.5, path weight: 0.5:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (3.5k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 10 Moves (4.4k Open)
    # With euclid weight 0.6, path weight: 0.4:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (3.5k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 10 Moves (4.4k Open)
    # With euclid weight 0.7, path weight: 0.3:
    # Heuristics.sum_shortest_distance_and_euclid: 1 --> 8 Moves (12k Open)
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 11 Moves (21k Open)

    # path and euclid equal

    # isInt = True, weight_path= 0.5, euclid_path= 0.5, no individual cast
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 1 --> 8 Moves (3.3k Open)
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 2 --> 10 Moves (3.8k Open)

    # isInt = False, weight_path= 0.5, euclid_path= 0.5, no individual cast
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 1 --> 8 Moves (1.6k Open)
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 2 --> 10 Moves (8.2k Open)

    # weight euclid more than path

    # isInt = True, weight_path= 0.7, euclid_path= 0.3, no individual cast
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 1 --> 8 Moves (7.8k Open)
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 2 --> 10 Moves (6.3k Open)
    # --> not so good

    # isInt = False, weight_path= 0.7, euclid_path= 0.3, no individual cast
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 1 --> 8 Moves (2.2k Open)
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 2 --> 10 Moves (4.0k Open)

    # Heuristics.harmonic_mean: 1 --> 8 Moves (17k Open)
    # Heuristics.harmonic_mean: 2 --> 12 Moves (15k Open)
    # --> not good

    # same with int
    # Heuristics.harmonic_mean: 1 --> 8 Moves (17k Open)
    # Heuristics.harmonic_mean: 2 --> 12 Moves (15k Open)
    # --> not good

    # Test: g = 2
    # isInt = True, weight_path= 0.5, euclid_path= 0.5, no individual cast
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 1 --> 8 Moves (12kk Open)
    # Heuristics.weighted_sum_shortest_distance_and_euclid: 2 --> stopped after 30k
    # --> not good

    # boardIndex = 1
    # field, spareTile = BoardHelper.readBoardFromCSV(f"data/puzzle_{boardIndex}.csv")
    # startColumn, endColumn = BoardHelper.readBoardInformation(f"data/info_{boardIndex}.txt")
    #
    # param = BoardHelper.generateBoard(field, spareTile, startColumn, endColumn)
    #
    # print(param)
    # alg = Algorithm()
    # path = alg.run(param)
    #
    # print(f"Took {len(path)} moves!")
    #
    # for step, node in enumerate(path):
    #     if node is not None:
    #         print(f"\n\n\n\n\n---------- [Step {step}] ----------\n")
    #         print(node)


if __name__ == "__main__":
    main()
