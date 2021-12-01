from Algorithm import Algorithm
from util import BoardHelper


def main():
    boardIndex = 2

    # heuristic_floor_euclid: 1 --> 8 Moves (50k Open)
    # heuristic_floor_euclid: 2 --> 11 Moves (9k Open)

    # heuristic_shortest_distance_end_path_player_path: 1 --> 8 Moves (11k Open)
    # heuristic_shortest_distance_end_path_player_path: 2 --> 10 Moves (7k Open)

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
