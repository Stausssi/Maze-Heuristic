class BoardHelper:
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

    @staticmethod
    def rotate(l, n):
        return l[-n:] + l[:-n]


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
