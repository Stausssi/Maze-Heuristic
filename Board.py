import random

from Tile import Tile
from util import BoardHelper, wrapInBorder


class Board:
    def __init__(self):
        self._tiles = []
        for r in range(5):
            column = []
            for c in range(4):
                rotatedList = [BoardHelper.rotate(valid, random.randint(0, 3)) for valid in BoardHelper.validTiles]
                column.append(
                    Tile(
                        tuple(rotatedList[random.randint(0, 2)]), r == 3 and c == 2
                    )
                )

            self._tiles.append(column)

        # create a random spare tile
        self.spareTile = Tile(
            [BoardHelper.rotate(valid, random.randint(0, 3)) for valid in BoardHelper.validTiles][random.randint(0, 2)]
        )

        # Set the start and end
        self.startTile = self._tiles[4][1]
        self.endTile = self._tiles[0][3]

    def did_player_win(self) -> bool:
        """
        Determines whether the player has won by checking whether he is on the endTile and the endTile has a connection
        to the top.

        Returns:
            True, if the player stands of the top right tile and the top is open.
        """

        return self.endTile.hasPlayer and self.endTile.topOpen

    def pushSpareTileIn(self, rowIndex):
        """
        This method handles the event of the spare tile being pushed into a given row.

        Args:
            rowIndex (int): The index of the row. 0 is the top row, 4 the lowest.

        Returns:
            None: Nothing
        """

        if rowIndex in range(5):
            tileRow = self._tiles[rowIndex]
            if rowIndex % 2 == 1:
                # Insert from the right
                outgoingTile = tileRow[0]
                tileRow.remove(outgoingTile)
                tileRow.append(self.spareTile)
            else:
                # Insert from the left
                tileRow.insert(0, self.spareTile)
                outgoingTile = tileRow.pop(len(tileRow) - 1)

            self.spareTile = outgoingTile
            self._tiles[rowIndex] = tileRow
        else:
            raise ValueError(f"Row index '{rowIndex}' is not in range [0, 4]")

    def __str__(self):
        """
        Returns: A string representing the board of tiles
        """

        output = "Board:\n"

        outputList = []
        for row in self._tiles:
            tileRow = [
                "",
                "",
                ""
            ]
            for tile in row:
                for rowIndex, charRow in enumerate(str(tile).split("\n")):
                    tileRow[rowIndex] += " " + charRow

            outputList.extend(tileRow)

        output += wrapInBorder(outputList)

        # Add the spare tile
        output += "\n\nSpare tile:\n"
        output += wrapInBorder(str(self.spareTile))

        return output


if __name__ == '__main__':
    board = Board()
    print(board)

    print("\nAfter pushing the spare Tile in:\n")
    board.pushSpareTileIn(4)
    print(board)

    print(wrapInBorder("KI\nAufgabe ist\nnervig.\n\n- Herr Reichhardt"))
