from itertools import product


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


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def floor_euclid_dist(x1, y1, x2, y2):
    return int(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)


def euclid_dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def min_distance_product(list1, list2):
    """
    
    Args:
        list1: 
        list2: 

    Returns:

    """

    list1 = list(list1)
    list2 = list(list2)

    distances = []

    for x1, y1 in list1:
        for x2, y2 in list2:
            distances.append(floor_euclid_dist(x1, y1, x2, y2))

    return min(distances)


# Heuristics

def heuristic_shortest_distance_end_path_player_path(node, player_pos, end_tile_pos):
    """

    Args:
        node:

    Returns:

    """

    player_row, player_column = player_pos
    endTile_row, endTile_column = end_tile_pos

    end_positions = node.get_reachable_positions(endTile_row, endTile_column)
    end_positions.add((endTile_row, endTile_column))

    player_positions = node.get_reachable_positions(player_row, player_column)
    player_positions.add((player_row, player_column))

    return min_distance_product(end_positions, player_positions)


def heuristic_floor_euclid(player_pos, end_tile_pos):
    player_row, player_column = player_pos
    endTile_row, endTile_column = end_tile_pos

    return floor_euclid_dist(player_row, player_column, endTile_row, endTile_column)


if __name__ == "__main__":
    import timeit

    list1 = [(1, 2), (1, 1), (5, 2)]
    list2 = [(3, 4), (2, 3)]

    print(min_distance_product(list1, list2))
