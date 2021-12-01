from config import tileEncodings


class Tile:
    def __init__(self, connections, hasPlayer=False):
        """

        Args:
            connections (tuple[bool, bool, bool, bool): The connections of the tile. Order is: Top, Right, Bottom, Left.
            hasPlayer (bool): Whether the player is standing on this Tile.
        """

        if isinstance(connections, tuple):
            self.connections = connections
        else:
            self.connections = tuple(connections)

        self.topOpen, self.rightOpen, self.bottomOpen, self.leftOpen = connections

        self.hasPlayer = hasPlayer

        self.representation = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ]

        if self.topOpen:
            self.representation[0][1] = "\u2551"

        if self.rightOpen:
            self.representation[1][2] = "\u2550"

        if self.bottomOpen:
            self.representation[2][1] = "\u2551"

        if self.leftOpen:
            self.representation[1][0] = "\u2550"

    def getRepresentation(self):
        """
        Creates the representation list.

        Returns:
            list[list[str]]: The representation of the tile as a list of list of strings.
        """

        # Determine the middle
        if self.hasPlayer:
            self.representation[1][1] = "\u25EF"
        else:
            from util import BoardHelper
            self.representation[1][1] = BoardHelper.middleConnectors.get(self.connections)

        return self.representation

    def getTileCode(self):
        """
        Get a code for a tile based on a predefined set of encodings.

        Returns:
            int: Code for the tile
        """

        return tileEncodings.get(self.connections)

    def __str__(self):
        """
        Returns: The string representation of the Tile.
        """

        return "\n".join([" ".join(line) for line in self.getRepresentation()])
