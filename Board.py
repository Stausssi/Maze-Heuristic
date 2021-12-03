import random

from Tile import Tile


class Board:
    """
    Represents the board of the game.

    Args:
        tiles: (list[list[Tile]] or None): The 2D list containing the tiles of the Board.
            Or None, if you wish to use a random board.
        spareTile (Tile): The spare tile in the beginning
        startTilePos (tuple[int, int]): A tuple containing the row and column of the start tile
        endTilePos (tuple[int, int]): A tuple containing the row and column of the end tile
    """

    def __init__(self, tiles=None, spareTile=None, startTilePos=None, endTilePos=None):
        self.notOnBoard = True

        if tiles is not None and spareTile is not None and startTilePos is not None and endTilePos is not None:
            self._tiles = tiles

            # create a random spare tile
            self._spareTile = spareTile

            # Set the start and end
            self._startTileRow = startTilePos[0]
            self._startTileColumn = startTilePos[1]
            self._endTileRow = endTilePos[0]
            self._endTileColumn = endTilePos[1]

            # the position of the player (tile) in the current board: (row, column)
            self._playerColumn = None
            self._playerRow = None
        else:
            self._tiles = []

            # create a random spare tile
            self._spareTile = None

            # Set the start and end
            self._startTileRow = None
            self._startTileColumn = None
            self._endTileRow = None
            self._endTileColumn = None

            # the position of the player (tile) in the current board: (row, column)
            self._playerColumn = None
            self._playerRow = None

    def initRandom(self):
        """
        Initialises the board with random tiles.

        Returns:
            None: Nothing
        """

        from util import BoardHelper

        self._tiles = []
        for r in range(5):
            column = []
            for c in range(4):
                # Rotate the list of valid tiles
                rotatedList = [BoardHelper.rotate(valid, random.randint(0, 3)) for valid in BoardHelper.validTiles]
                # Select a random tile out of the list
                column.append(
                    Tile(
                        tuple(rotatedList[random.randint(0, 2)])
                    )
                )

            # Save the column
            self._tiles.append(column)

        # create a random spare tile
        self._spareTile = Tile(
            tuple(
                [
                    BoardHelper.rotate(valid, random.randint(0, 3)) for valid in BoardHelper.validTiles
                ][random.randint(0, 2)]
            )
        )

        # Set the start and end
        self._startTileRow = 4
        self._startTileColumn = 1
        self._endTileRow = 0
        self._endTileColumn = 3

        # the position of the player (tile) in the current board: (row, column)
        self._playerColumn = 1
        self._playerRow = 4

        self.setPlayerPosition(self._startTileColumn, self._startTileRow)

    def getAdjacentTile(self, position, relative_position):
        """
        Get the tile that is left/right/top/bottom of a given tile, or None, if it is outside the border.

        Args:
            position (tuple[int, int]): Position of the current tile in the board
            relative_position (str): Position of tile relative to the given tile (right, left, top, bottom)

        Returns:
            tuple[Tile, tuple[int,int]]: The neighbouring tile and it´s position on the board
        """

        column = position[1]
        row = position[0]
        adjacent_column = column
        adjacent_row = row

        if relative_position == "top":
            adjacent_row = row - 1
        elif relative_position == "bottom":
            adjacent_row = row + 1
        elif relative_position == "left":
            adjacent_column = column - 1
        elif relative_position == "right":
            adjacent_column = column + 1
        else:
            raise ValueError(f"The argument {relative_position} for relative position is not allowed.")

        # check if new column/row is valid
        board_height = len(self._tiles)
        board_width = len(self._tiles[0])
        if board_width > adjacent_column >= 0 and board_height > adjacent_row >= 0:
            return self._tiles[adjacent_row][adjacent_column], (adjacent_row, adjacent_column)
        else:
            # adjacent tile does not exist
            return None, None

    def get_reachable_positions(self, row, column):
        """
        Return a set of tuples, with the positions a player could move to by following the connected pieces.
        This is without the current position of the player.

        Args:
            row (int): The row of the starting tile
            column (int): The column of the starting tile

        Returns:
            set[tuple[int,int]]: Possible positions, the player could move to, except the current.

        """

        open_set = {(row, column)}
        closed_set = set()

        while len(open_set) != 0:
            # copy the open set, so that it isn´t change during iteration
            open_set_copy = open_set.copy()

            for position in open_set_copy:
                # get the tile at "position"
                position_tile = self._tiles[position[0]][position[1]]

                # remove position from open_set and put it into the closed set
                open_set.remove(position)
                closed_set.add(position)

                # expand "position", put all neighbours in open_set, that are reachable from "position"

                # top
                neighbour_tile, neighbour_position = self.getAdjacentTile(position, relative_position="top")
                if neighbour_position is not None \
                        and neighbour_position not in open_set \
                        and neighbour_position not in closed_set:
                    # check if tile can be walked to
                    if position_tile.topOpen and neighbour_tile.bottomOpen:
                        open_set.add(neighbour_position)

                # bottom
                neighbour_tile, neighbour_position = self.getAdjacentTile(position, relative_position="bottom")
                if neighbour_position is not None \
                        and neighbour_position not in open_set \
                        and neighbour_position not in closed_set:
                    # check if tile can be walked to
                    if position_tile.bottomOpen and neighbour_tile.topOpen:
                        open_set.add(neighbour_position)

                # left
                neighbour_tile, neighbour_position = self.getAdjacentTile(position, relative_position="left")
                if neighbour_position is not None \
                        and neighbour_position not in open_set \
                        and neighbour_position not in closed_set:
                    # check if tile can be walked to
                    if position_tile.leftOpen and neighbour_tile.rightOpen:
                        open_set.add(neighbour_position)

                # right
                neighbour_tile, neighbour_position = self.getAdjacentTile(position, relative_position="right")
                if neighbour_position is not None \
                        and neighbour_position not in open_set \
                        and neighbour_position not in closed_set:
                    # check if tile can be walked to
                    if position_tile.rightOpen and neighbour_tile.leftOpen:
                        open_set.add(neighbour_position)

        return closed_set - {(row, column)}

    def setPlayerPosition(self, column, row):
        """
        Set the position of the player in the current board.

        Args:
            column(int): Column
            row(int): Row

        Returns:
            None: Nothing

        """

        if self.notOnBoard:
            self.notOnBoard = False
        else:
            # reset current tile
            self._tiles[self._playerRow][self._playerColumn].hasPlayer = False

        # set new board position
        self._playerColumn, self._playerRow = column, row
        self._tiles[row][column].hasPlayer = True

    def didPlayerWin(self):
        """
        Determines whether the player has won by checking whether he is on the endTile and the endTile has a connection
        to the top.

        Returns:
            bool: True, if the player stands of the top right tile and the top is open.
        """

        endTile = self.getEndTile()

        return endTile.hasPlayer and endTile.topOpen

    def getEndTile(self):
        """
        Returns the end tile.

        Returns:
            Tile: The end tile
        """

        return self._tiles[self._endTileRow][self._endTileColumn]

    def getStartTile(self):
        """
        Return the start Tile.

        Returns:
            Tile: The start tile
        """

        return self._tiles[self._startTileRow][self._startTileColumn]

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
                tileRow.append(self._spareTile)
            else:
                # Insert from the left
                tileRow.insert(0, self._spareTile)
                outgoingTile = tileRow.pop(len(tileRow) - 1)

            # if player is pushed out of the board, place him on the spareTile
            if outgoingTile.hasPlayer:
                self._spareTile.hasPlayer = True
                outgoingTile.hasPlayer = False

            self._spareTile = outgoingTile
            self._tiles[rowIndex] = tileRow

            # update the position of the player
            for row in range(self.getSize()[0]):
                for column in range(self.getSize()[1]):
                    if self._tiles[row][column].hasPlayer:
                        self._playerRow = row
                        self._playerColumn = column
                        return

        else:
            raise ValueError(f"Row index '{rowIndex}' is not in range [0, 4]")

    def getPlayerPosition(self):
        """
        Get the position of the current player on the board.

        Returns:
            tuple[int, int]: Position (row, column) of the current player

        """

        return self._playerRow, self._playerColumn

    def getSize(self):
        """
        Returns the number of rows and columns of the board: (rows, columns)

        Returns:
            tuple[int, int]: Number of rows and column of the board: (rows, columns)

        """

        return len(self._tiles), len(self._tiles[0])

    def getEndTilePosition(self):
        """
        Gets the position of the end tile.

        Returns:
            tuple[int, int]: The row and column of the end tile.
        """

        return self._endTileRow, self._endTileColumn

    def getStartTilePosition(self):
        """
        Gets the position of the start tile.

        Returns:
            tuple[int, int]: The row and column of the start tile.
        """

        return self._startTileRow, self._startTileColumn

    def generateKey(self):
        """
        Generate a string for a dictionary, that encodes the whole information of the board, including the player
        position, all tiles and the spare tile.

        The first (board_height * board_width) characters are tile codes for each tile of the board, from left to right
        and from top to bottom. After that the code of the spare tile follows.
        Finally, the position of the player is encoded as follows:
            row column start
        where start is either 0 or 1, depending on whether the player is not on the board yet

        Returns:
            str: encoded String of the board
        """

        key = ""

        # encode the tiles
        for row in self._tiles:
            for tile in row:
                key += str(tile.getTileCode())

        # encode the spare tile
        key += str(self._spareTile.getTileCode())

        # encode the position of the player
        key += str(self._playerRow)
        key += str(self._playerColumn)

        return key

    def __str__(self):
        """
        Returns:
            str: A string representing the board of tiles
        """

        from util import wrapInBorder

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
        output += wrapInBorder(str(self._spareTile))

        return output
