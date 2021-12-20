import time

from Algorithm import Algorithm
from util import BoardHelper
import argparse


def main():
    """
    Run the algorithm on both of the given boards.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="puzzle_x.txt file")
    parser.add_argument("-i", help="info_x.txt file")
    args = parser.parse_args()

    field, spareTile, startPos, endPos = None, None, None, None

    try:
        field, spareTile = BoardHelper.readBoardFromCSV(f"data/{args.p}")
    except FileNotFoundError:
        print(f"The file {args.p} was not found in the folder data.")
        exit(1)

    try:
        startPos, endPos = BoardHelper.readBoardInformation(f"data/{args.i}")
    except FileNotFoundError:
        print(f"The file {args.i} was not found in the folder data.")
        exit(1)

    board = BoardHelper.generateBoard(field, spareTile, startPos, endPos)
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
