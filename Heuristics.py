from scipy.spatial import distance


class Heuristics:
    @staticmethod
    def euclid(player_pos, end_tile_pos):
        # player_row, player_column = player_pos
        # endTile_row, endTile_column = end_tile_pos

        # return HeuristicHelpers.floor_euclid_dist(player_row, player_column, endTile_row, endTile_column)

        return int(distance.euclidean(player_pos, end_tile_pos))

    @staticmethod
    def manhattan(player_pos, end_tile_pos):
        return int(distance.cityblock(player_pos, end_tile_pos))
        # return int(HeuristicHelpers.manhattan_dist(*player_pos, *end_tile_pos))

    @staticmethod
    def minkowski(player_pos, end_tile_pos, norm):
        return int(distance.minkowski(player_pos, end_tile_pos, p=norm))

    @staticmethod
    def chebyshev(player_pos, end_tile_pos):
        return int(distance.chebyshev(player_pos, end_tile_pos))

    @staticmethod
    def shortest_distance_end_path_player_path(node, player_pos, end_tile_pos):
        """

        Args:
            node:
            player_pos:
            end_tile_pos:

        Returns:

        """

        player_row, player_column = player_pos
        endTile_row, endTile_column = end_tile_pos

        end_positions = node.get_reachable_positions(endTile_row, endTile_column)
        end_positions.add((endTile_row, endTile_column))

        player_positions = node.get_reachable_positions(player_row, player_column)
        player_positions.add((player_row, player_column))

        return HeuristicHelpers.min_distance_product(end_positions, player_positions)


class HeuristicHelpers:
    @staticmethod
    def manhattan_dist(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def floor_euclid_dist(x1, y1, x2, y2):
        return int(HeuristicHelpers.euclid_dist(x1, y1, x2, y2))

    @staticmethod
    def euclid_dist(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    @staticmethod
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
                distances.append(HeuristicHelpers.floor_euclid_dist(x1, y1, x2, y2))

        return min(distances)


if __name__ == "__main__":
    list1 = [(1, 2), (1, 1), (5, 2)]
    list2 = [(3, 4), (2, 3)]

    print(HeuristicHelpers.min_distance_product(list1, list2))
