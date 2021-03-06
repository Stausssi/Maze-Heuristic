class Tile:
    """
    Represents a graphical Tile in the Board.

    Args:
        connections (tuple[bool, bool, bool, bool]): The connections of the tile. Order is: Top, Right, Bottom, Left.
        hasPlayer (bool): Whether the player is standing on this Tile.
    """

    def __init__(self, connections, hasPlayer=False):
        if isinstance(connections, tuple):
            self.connections = connections
        else:
            self.connections = tuple(connections)

        self.topOpen, self.rightOpen, self.bottomOpen, self.leftOpen = connections

        self.hasPlayer = hasPlayer

        # Create a list containing a character for every field in the 3x3 matrix
        self.representation = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ]

        # Set the characters depending on the connections
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
            list[list[str]]: The representation of the tile as a list of a list of strings.
        """

        from util import BoardHelper

        # Determine the middle
        if self.hasPlayer:
            self.representation[1][1] = "\u25EF"
        else:
            self.representation[1][1] = BoardHelper.middleConnectors.get(self.connections)

        return self.representation

    def getTileCode(self):
        """
        Get a code for a tile based on a predefined set of encodings.

        Returns:
            int: Code for the tile
        """

        from util import BoardHelper

        return BoardHelper.tileEncodings.get(self.connections)

    def __str__(self):
        """
        Returns:
            str: The string representation of the Tile.
        """

        return "\n".join([" ".join(line) for line in self.getRepresentation()])
