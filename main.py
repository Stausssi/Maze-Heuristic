import time

from Algorithm import Algorithm
from util import BoardHelper


def main():
    """
    Run the algorithm on both of the given boards.
    """

    for boardIndex in range(1, 3):
        field, spareTile = BoardHelper.readBoardFromCSV(f"data/puzzle_{boardIndex}.csv")
        startColumn, endColumn = BoardHelper.readBoardInformation(f"data/info_{boardIndex}.txt")

        board = BoardHelper.generateBoard(field, spareTile, startColumn, endColumn)
        print("Solving", board)

        alg = Algorithm()
        start = time.time()
        path, openCount = alg.run(board)
        end = time.time()

        for step, node in enumerate(path):
            if node is not None:
                print(f"\n\n---------- [Step {step}] ----------\n")
                print(node)

        print(f"{openCount} Nodes were opened! Calculation took {round(end - start,2)} seconds.\n\n")


if __name__ == "__main__":
    main()
