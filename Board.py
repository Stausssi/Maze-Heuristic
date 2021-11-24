import random

from Tile import Tile


def rotate(list, n):
    return list[-n:] + list[:-n]


validTiles = [
    [True, True, True, False],  # Top-Right-Bottom
    [True, False, True, False],  # Top-Bottom
    [True, False, False, True]  # Top-Left
]


class Board:
    def __init__(self):
        self._tiles = []
        for r in range(5):
            column = []
            for c in range(4):
                hasPlayer = r == 3 and c == 3
                rotatedList = [rotate(valid, random.randint(0, 3)) for valid in validTiles]
                column.append(
                    Tile(
                        rotatedList[random.randint(0, 2)], hasPlayer
                    )
                )

            self._tiles.append(column)

    def __str__(self):
        """
        Returns: A string representing the board of tiles
        """

        output = ""
        for row in self._tiles:

            tileRow = [
                "",
                "",
                ""
            ]
            for tile in row:
                for rowIndex, charRow in enumerate(tile.representation):
                    tileRow[rowIndex] += " ".join(charRow) + " "

            output += "\n"
            output += "\n".join([charRow for charRow in tileRow])

        return output


if __name__ == '__main__':
    print(Board())
