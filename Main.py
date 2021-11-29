from Algorithm import Algorithm
from Board import Board


def main():
    board = Board()
    board.setPlayerPosition(2, 2)
    alg = Algorithm()
    path = alg.run(board)

    print(len(path))
    for node in path:
        print(node)


if __name__ == "__main__":
    main()
