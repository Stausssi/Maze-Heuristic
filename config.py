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

# startColumn = 1
#
# endColumn = 3
