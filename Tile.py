class Tile:
    def __init__(self, connections, hasPlayer=False):
        self.connections = connections
        self.topOpen, self.rightOpen, self.bottomOpen, self.leftOpen = connections

        self.hasPlayer = hasPlayer

    def getRepresentation(self):
        """
        Creates the representation list.

        Returns:
            list[list[str]]: The representation of the tile as a list of list of strings.
        """

        representation = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ]

        if self.topOpen:
            representation[0][1] = "\u2551"

        if self.rightOpen:
            representation[1][2] = "\u2550"

        if self.bottomOpen:
            representation[2][1] = "\u2551"

        if self.leftOpen:
            representation[1][0] = "\u2550"

        if all(self.connections):
            representation[1][1] = "\u256C"

        # Determine the middle
        if self.leftOpen and self.topOpen and self.rightOpen and not self.bottomOpen:
            representation[1][1] = "\u2569"

        if self.leftOpen and self.bottomOpen and self.rightOpen and not self.topOpen:
            representation[1][1] = "\u2566"

        if self.leftOpen and self.rightOpen and not self.topOpen and not self.bottomOpen:
            representation[1][1] = "\u2550"

        if self.topOpen and self.bottomOpen and not self.leftOpen and not self.rightOpen:
            representation[1][1] = "\u2551"

        if self.topOpen and self.rightOpen and self.bottomOpen and not self.leftOpen:
            representation[1][1] = "\u2560"

        if self.leftOpen and self.bottomOpen and not self.rightOpen and not self.topOpen:
            representation[1][1] = "\u2557"

        if self.rightOpen and self.bottomOpen and not self.leftOpen and not self.topOpen:
            representation[1][1] = "\u2554"

        if self.leftOpen and self.topOpen and not self.rightOpen and not self.bottomOpen:
            representation[1][1] = "\u255D"

        if self.rightOpen and self.topOpen and not self.leftOpen and not self.bottomOpen:
            representation[1][1] = "\u255A"

        if self.leftOpen and self.topOpen and self.bottomOpen and not self.rightOpen:
            representation[1][1] = "\u2563"

        if self.hasPlayer:
            representation[1][1] = "O"

        return representation

    def __str__(self):
        """
        Returns: The string representation of the Tile.
        """

        output = "_" * 9
        output += "\n| "
        output += "\n| ".join([" ".join(line) + " |" for line in self.getRepresentation()])
        output += "\n"
        output += "-" * 9
        return output
