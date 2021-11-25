class Tile:
    def __init__(self, connections, hasPlayer=False):
        self.connections = connections
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
            self.representation[1][1] = "O"
        else:
            if all(self.connections):
                self.representation[1][1] = "\u256C"

            if self.leftOpen and self.topOpen and self.rightOpen and not self.bottomOpen:
                self.representation[1][1] = "\u2569"

            if self.leftOpen and self.bottomOpen and self.rightOpen and not self.topOpen:
                self.representation[1][1] = "\u2566"

            if self.leftOpen and self.rightOpen and not self.topOpen and not self.bottomOpen:
                self.representation[1][1] = "\u2550"

            if self.topOpen and self.bottomOpen and not self.leftOpen and not self.rightOpen:
                self.representation[1][1] = "\u2551"

            if self.topOpen and self.rightOpen and self.bottomOpen and not self.leftOpen:
                self.representation[1][1] = "\u2560"

            if self.leftOpen and self.bottomOpen and not self.rightOpen and not self.topOpen:
                self.representation[1][1] = "\u2557"

            if self.rightOpen and self.bottomOpen and not self.leftOpen and not self.topOpen:
                self.representation[1][1] = "\u2554"

            if self.leftOpen and self.topOpen and not self.rightOpen and not self.bottomOpen:
                self.representation[1][1] = "\u255D"

            if self.rightOpen and self.topOpen and not self.leftOpen and not self.bottomOpen:
                self.representation[1][1] = "\u255A"

            if self.leftOpen and self.topOpen and self.bottomOpen and not self.rightOpen:
                self.representation[1][1] = "\u2563"

        return self.representation

    def __str__(self):
        """
        Returns: The string representation of the Tile with a border around it.
        """

        output = "_" * 9
        output += "\n| "
        output += "\n| ".join([" ".join(line) + " |" for line in self.getRepresentation()])
        output += "\n"
        output += "-" * 9
        return output
