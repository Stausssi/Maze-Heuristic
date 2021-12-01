from Algorithm import Algorithm
from Board import Board, generateBord
from config import field, spareTile, startColumn, endColumn


def main():
    board = generateBord(field, spareTile, startColumn, endColumn)

    # board.setPlayerPosition(2, 3)
    board.setPlayerPosition(column=1, row=4)
    print(board)
    alg = Algorithm()
    path = alg.run(board)

    print(f"Took {len(path)} moves!")

    for node in path:
        if node is not None:
            print(node)


if __name__ == "__main__":
    main()
