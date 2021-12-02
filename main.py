from Algorithm import Algorithm
from util import BoardHelper


def main():
    boardIndex = 2

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
    # Heuristics.sum_shortest_distance_and_euclid: 2 --> 11 Moves (8.7 Open)

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

    field, spareTile = BoardHelper.readBoardFromCSV(f"data/puzzle_{boardIndex}.csv")
    startColumn, endColumn = BoardHelper.readBoardInformation(f"data/info_{boardIndex}.txt")

    board = BoardHelper.generateBoard(field, spareTile, startColumn, endColumn)

    print(board)
    alg = Algorithm()
    path = alg.run(board)

    print(f"Took {len(path)} moves!")

    for step, node in enumerate(path):
        if node is not None:
            print(f"\n\n\n\n\n---------- [Step {step}] ----------\n")
            print(node)


if __name__ == "__main__":
    main()
