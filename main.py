from Algorithm import Algorithm
# from config import startColumn, endColumn
from util import BoardHelper


def main():
    boardIndex = 1

    field, spareTile = BoardHelper.readBoardFromCSV(f"data/puzzle_{boardIndex}.csv")
    startColumn, endColumn = BoardHelper.readBoardInformation(f"data/info_{boardIndex}.txt")

    board = BoardHelper.generateBoard(field, spareTile, startColumn, endColumn)

    # board.setPlayerPosition(2, 3)
    # board.setPlayerPosition(column=1, row=4)
    print(board)
    alg = Algorithm()
    path = alg.run(board)

    print(f"Took {len(path)} moves!")

    for node in path:
        if node is not None:
            print(node)


if __name__ == "__main__":
    main()
