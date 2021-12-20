import csv
from typing import Tuple, List

from Tile import Tile
from Board import Board


class BoardHelper:
    """
    Basic class containing helpful functions and variables for the board.
    """

    middleConnectors = {
        # # Cross in the middle
        # (True, True, True, True): "\u256C",

        # Intersection towards the top
        (True, True, False, True): "\u2569",
        # Intersection towards the right
        (True, True, True, False): "\u2560",
        # Intersection towards the bottom
        (False, True, True, True): "\u2566",
        # Intersection towards the left
        (True, False, True, True): "\u2563",

        # From Top to Bottom
        (True, False, True, False): "\u2551",
        # From Right to Left
        (False, True, False, True): "\u2550",

        # From Top to Right
        (True, True, False, False): "\u255A",
        # From Right to Bottom
        (False, True, True, False): "\u2554",
        # From Bottom to Left
        (False, False, True, True): "\u2557",
        # From Left to Top
        (True, False, False, True): "\u255D",
    }

    validTiles = [
        # Intersection
        [True, True, True, False],
        # Straight connection
        [True, False, True, False],
        # Corner
        [True, False, False, True]
    ]

    tileEncodings = {
        # True in the Tuple indicates positions where the tile is open
        # based on: (top, right, bottom, left)

        # Corner 1
        (False, True, True, False): 0,
        # Corner 2
        (False, False, True, True): 1,
        # Corner 3
        (True, True, False, False): 2,
        # Corner 4
        (True, False, False, True): 3,
        # Intersection 1
        (False, True, True, True): 4,
        # Intersection 2
        (True, False, True, True): 5,
        # Intersection 3
        (True, True, False, True): 6,
        # Intersection 4
        (True, True, True, False): 7,
        # Line 1
        (True, False, True, False): 8,
        # Line 2
        (False, True, False, True): 9,
    }

    reversedTileEncodings = dict((v, k) for (k, v) in tileEncodings.items())

    @staticmethod
    def rotate(listToRotate, n):
        """
        Rotates the list n times.

        Args:
            listToRotate (list): The list to rotate
            n (int): The number of rotations

        Returns:
            list: The rotated list.
        """

        return listToRotate[-n:] + listToRotate[:-n]

    @staticmethod
    def readBoardFromCSV(path) -> Tuple[List[List[int]], int]:
        """
        Reads a param from a given CSV and returns the tiles list and a spare tile

        Args:
            path (str): The path to the CSV file

        Returns:
            tuple: The Tiles of the Board and the spare Tile
        """

        with open(path) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=";")

            tiles = []
            spareTile = None
            for rowCount, row in enumerate(csvReader):
                # First 4 lines are tiles
                if rowCount <= 4:
                    rowList = []
                    for encodedTile in row:
                        rowList.append(int(encodedTile))
                    tiles.append(rowList)
                else:
                    # Last row contains the spare tile
                    spareTile = int(row[0])

            return tiles, spareTile

    @staticmethod
    def readBoardInformation(filepath) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Reads the textfile at the given path and decodes the information for start and end.

        Args:
            filepath (str): The path to the file

        Returns:
            tuple[tuple[int, int], tuple[int, int]]: A tuple containing the position of the start and end point in that order
        """

        mapping = {
            "Startposition:": 0,
            "Zielposition": 0
        }
        nextValue = ""

        with open(filepath) as informationFile:
            for line in informationFile:
                line = line.strip().strip("\n").strip("\t")
                if len(line) > 0:
                    # Check if line value has a dict entry
                    if mapping.get(line) is not None:
                        nextValue = line
                    elif nextValue != "":
                        # Extract the integer out of the line
                        lineContent = line.replace("Spalte ", "").split(" ")

                        value = int(lineContent[0]) - 1

                        if lineContent[1] == "oben":
                            value = (0, value)
                        elif lineContent[1] == "unten":
                            value = (4, value)
                        else:
                            raise ValueError(
                                f"Invalid information file. Expected 'oben' or 'unten', not '{lineContent[1]}'"
                            )

                        mapping.update({
                            nextValue: value
                        })

                        nextValue = ""

        return mapping.get("Startposition:"), mapping.get("Zielposition")

    @staticmethod
    def generateBoard(tile_codes, spareTile_code, startTile_pos, endTile_pos):
        """
        Generates a Board object with the given codes and positions.

        Args:
            tile_codes (list[list[int]]): The encoded tile representation of the board.
            spareTile_code (int): The encoded spare tile.
            startTile_pos (tuple[int, int]): The position (row, col) of the start tile
            endTile_pos (tuple[int, int]): The position (row, col) of the end tile

        Returns:
            Board: A board with the given specifications.
        """

        from Board import Board

        tiles = []
        # Go over every encoded tile, decode it and save it
        for r in tile_codes:
            column = []
            for tile_code in r:
                column.append(
                    Tile(
                        BoardHelper.reversedTileEncodings.get(tile_code)
                    )
                )

            tiles.append(column)

        # get the spare tile
        spareTile = Tile(BoardHelper.reversedTileEncodings.get(spareTile_code))

        return Board(tiles=tiles, spareTile=spareTile, startTilePos=startTile_pos, endTilePos=endTile_pos)


def wrapInBorder(message) -> str:
    """
    Wraps a given list of strings into a border.

    Args:
        message (list[str] or str): A list containing a string for every row of the desired output,
         or a str which will be split at every linebreak

    Returns:
        str: A string containing the given strings with a border around it.
    """

    # Split at newline if input is a string
    if isinstance(message, str):
        message = message.split("\n")

    # Determine the longest line
    maxLength = max([len(line) for line in message])

    # Add the upper border
    output = "\u250F" + "\u2501" * (maxLength + 2) + "\u2513\n"

    # First left border -> separate
    output += "\u2503 "

    # Add the left border, add the line contents, fill with padding (if needed) and add the right border
    output += "\u2503 ".join(
        [line + " " * (maxLength - len(line)) + " \u2503\n" for line in message]
    )

    # Add the lower Border
    output += "\u2517" + "\u2501" * (maxLength + 2) + "\u251B"

    return output
