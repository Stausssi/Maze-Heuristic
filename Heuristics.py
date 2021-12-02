from decimal import getcontext

from scipy.spatial import distance

getcontext().prec = 2 * 1000


class Heuristics:
    @staticmethod
    def euclid_int(player_pos, end_tile_pos):

        return int(distance.euclidean(player_pos, end_tile_pos))

    @staticmethod
    def euclid(player_pos, end_tile_pos):

        return distance.euclidean(player_pos, end_tile_pos)

    @staticmethod
    def manhattan_int(player_pos, end_tile_pos):
        return int(distance.cityblock(player_pos, end_tile_pos))
        # return int(HeuristicHelpers.manhattan_dist(*player_pos, *end_tile_pos))

    @staticmethod
    def manhattan(player_pos, end_tile_pos):
        return distance.cityblock(player_pos, end_tile_pos)
        # return int(HeuristicHelpers.manhattan_dist(*player_pos, *end_tile_pos))

    @staticmethod
    def minkowski_int(player_pos, end_tile_pos, norm):
        return int(distance.minkowski(player_pos, end_tile_pos, p=norm))

    @staticmethod
    def minkowski(player_pos, end_tile_pos, norm):
        return distance.minkowski(player_pos, end_tile_pos, p=norm)

    @staticmethod
    def chebyshev_int(player_pos, end_tile_pos):
        return int(distance.chebyshev(player_pos, end_tile_pos))

    @staticmethod
    def chebyshev(player_pos, end_tile_pos):
        return distance.chebyshev(player_pos, end_tile_pos)

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

        for point1 in list1:
            for point2 in list2:
                distances.append(Heuristics.euclid(point1, point2))

        return min(distances)

    @staticmethod
    def shortest_distance_end_path_player_path(node, player_pos, end_tile_pos, isInt=True):
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

        if isInt:
            return int(Heuristics.min_distance_product(end_positions, player_positions))
        else:
            return Heuristics.min_distance_product(end_positions, player_positions)

    @staticmethod
    def min_shortest_distance_and_euclid(node, player_pos, end_tile_pos):
        return min(
            Heuristics.euclid_int(player_pos, end_tile_pos),
            Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos)
        )

    @staticmethod
    def sum_shortest_distance_and_euclid_int(node, player_pos, end_tile_pos, weight_euclid=1, weight_path=1):
        return int(Heuristics.euclid(player_pos, end_tile_pos) * weight_euclid + \
                   Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos, isInt=False) \
                   * weight_path)

    @staticmethod
    def sum_shortest_distance_and_euclid(node, player_pos, end_tile_pos, weight_euclid=1, weight_path=1):
        return Heuristics.euclid(player_pos, end_tile_pos) * weight_euclid + \
                   Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos, isInt=False) \
                   * weight_path

    @staticmethod
    def harmonic_mean(node, player_pos, end_tile_pos):

        player_row, player_column = player_pos
        endTile_row, endTile_column = end_tile_pos

        end_positions = node.get_reachable_positions(endTile_row, endTile_column)
        end_positions.add((endTile_row, endTile_column))

        player_positions = node.get_reachable_positions(player_row, player_column)
        player_positions.add((player_row, player_column))

        min_dist = Heuristics.min_distance_product(end_positions, player_positions)
        player_to_end = Heuristics.euclid(end_positions, player_positions)

        try:
            return (min_dist * player_to_end) / (min_dist + player_to_end)
        except ZeroDivisionError:
            return 0


if __name__ == "__main__":
    list1 = [(1, 2), (1, 1), (5, 2)]
    list2 = [(3, 4), (2, 3)]

    print(Heuristics.min_distance_product(list1, list2))
