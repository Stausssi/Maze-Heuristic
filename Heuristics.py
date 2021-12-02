from scipy.spatial import distance
from decimal import Decimal, getcontext

getcontext().prec = 2*1000


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

        return int(HeuristicHelpers.min_distance_product(end_positions, player_positions))

    @staticmethod
    def min_shortest_distance_and_euclid(node, player_pos, end_tile_pos):
        return min(
            Heuristics.euclid(player_pos, end_tile_pos),
            Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos)
        )

    @staticmethod
    def sum_shortest_distance_and_euclid(node, player_pos, end_tile_pos):
        return Heuristics.euclid(player_pos, end_tile_pos) + \
               Heuristics.shortest_distance_end_path_player_path(node, player_pos, end_tile_pos)

    @staticmethod
    def weighted_sum_shortest_distance_and_euclid(node, player_pos, end_tile_pos, weigth_path, weigth_euclid,
                                                  isInt=True):

        player_row, player_column = player_pos
        endTile_row, endTile_column = end_tile_pos

        end_positions = node.get_reachable_positions(endTile_row, endTile_column)
        end_positions.add((endTile_row, endTile_column))

        player_positions = node.get_reachable_positions(player_row, player_column)
        player_positions.add((player_row, player_column))

        min_dist = HeuristicHelpers.min_distance_product(end_positions, player_positions)
        player_to_end = HeuristicHelpers.euclid_dist(player_row, player_column, endTile_row, endTile_column)

        if isInt:
            return int(min_dist * weigth_path + player_to_end * weigth_euclid)
        else:
            return min_dist * weigth_path + player_to_end * weigth_euclid

    @staticmethod
    def harmonic_mean(node, player_pos, end_tile_pos):

        player_row, player_column = player_pos
        endTile_row, endTile_column = end_tile_pos

        end_positions = node.get_reachable_positions(endTile_row, endTile_column)
        end_positions.add((endTile_row, endTile_column))

        player_positions = node.get_reachable_positions(player_row, player_column)
        player_positions.add((player_row, player_column))

        min_dist = HeuristicHelpers.min_distance_product(end_positions, player_positions)
        player_to_end = HeuristicHelpers.euclid_dist(player_row, player_column, endTile_row, endTile_column)

        try:
            return (min_dist * player_to_end) / (min_dist + player_to_end)
        except ZeroDivisionError:
            return 0


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
                distances.append(HeuristicHelpers.euclid_dist(x1, y1, x2, y2))

        return min(distances)


if __name__ == "__main__":
    list1 = [(1, 2), (1, 1), (5, 2)]
    list2 = [(3, 4), (2, 3)]

    print(HeuristicHelpers.min_distance_product(list1, list2))
