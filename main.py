from Algorithm import Algorithm
from util import BoardHelper


def main():
    for boardIndex in range(1, 3):
        field, spareTile = BoardHelper.readBoardFromCSV(f"data/puzzle_{boardIndex}.csv")
        startColumn, endColumn = BoardHelper.readBoardInformation(f"data/info_{boardIndex}.txt")

        board = BoardHelper.generateBoard(field, spareTile, startColumn, endColumn)

        alg = Algorithm()
        path, openCount = alg.run(board)

        print(f"Took {len(path)} moves for Board {boardIndex}!")
        print(f"{openCount} Nodes were opened!")

        for step, node in enumerate(path):
            if node is not None:
                print(f"\n\n---------- [Step {step}] ----------\n")
                print(node)

        print("\n\n")


if __name__ == "__main__":
    main()
