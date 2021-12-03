var = {'minkowski': (7.380952380952381, 1.6874889770363088, 1160.7619047619048, 1412.7905685119047),
       'minkowski_int': (7.523809523809524, 1.8335497707738293, 1787.7619047619048, 2595.1133868245893),
       'euclid': (7.428571428571429, 1.91236577493503, 1167.857142857143, 1507.7458103312467),
       'euclid_int': (7.476190476190476, 1.7781745588959375, 1665.6666666666667, 2070.8629924100082),
       'manhattan': (7.714285714285714, 1.8746428231227714, 1997.904761904762, 2246.581645628796),
       'chebyshev': (7.476190476190476, 1.7781745588959375, 1756.8095238095239, 2301.7656835361768),
       'shortest_distance': (6.619047619047619, 1.3955712262794213, 1527.8095238095239, 2695.9228775884453),
       'shortest_distance_int': (6.619047619047619, 1.3955712262794213, 2072.904761904762, 3825.014521603309),
       'min_shortest_distance': (6.619047619047619, 1.3955712262794213, 2072.904761904762, 3825.014521603309),
       'sum_shortest_distance': (7.428571428571429, 2.0389072703639215, 363.85714285714283, 440.5737492990573),
       'sum_shortest_distance_0.1_0.9': (6.619047619047619, 1.3955712262794213, 742.1904761904761, 1189.3587608054863),
       'sum_shortest_distance_0.2_0.8': (6.619047619047619, 1.3955712262794213, 674.1904761904761, 1049.0734778387841),
       'sum_shortest_distance_0.3_0.7': (6.619047619047619, 1.3955712262794213, 592.047619047619, 765.3846403077655),
       'sum_shortest_distance_0.4_0.6': (6.619047619047619, 1.3955712262794213, 749.9047619047619, 957.9552131891086),
       'sum_shortest_distance_0.5_0.5': (6.9523809523809526, 1.5961262630566064, 922.0952380952381, 1279.6156807714533),
       'sum_shortest_distance_0.6_0.4': (7.142857142857143, 1.590148241067929, 847.7142857142857, 1061.297655837284),
       'sum_shortest_distance_0.7_0.34': (
       7.190476190476191, 1.6315344807587615, 897.1904761904761, 1130.711086840826),
       'sum_shortest_distance_0.8_0.2': (
       7.190476190476191, 1.6315344807587615, 903.1428571428571, 1212.707313646384),
       'sum_shortest_distance_0.9_0.1': (
       7.285714285714286, 1.7647338933351153, 990.047619047619, 1300.8802203197063),
       'sum_shortest_distance_int_0.1_0.9': (
       6.619047619047619, 1.3955712262794213, 1981.904761904762, 3492.0322865741364),
       'sum_shortest_distance_int_0.2_0.8': (
       6.619047619047619, 1.3955712262794213, 1816.952380952381, 3150.2906132004787),
       'sum_shortest_distance_int_0.3_0.7': (
       6.619047619047619, 1.3955712262794213, 1213.3809523809523, 1725.4059080746906),
       'sum_shortest_distance_int_0.4_0.6': (
       6.619047619047619, 1.3955712262794213, 871.047619047619, 1206.2075474888422),
       'sum_shortest_distance_int_0.5_0.5': (
       7.0476190476190474, 1.6271505915615332, 1961.3809523809523, 3461.128594493283),
       'sum_shortest_distance_int_0.6_0.4': (
       7.0476190476190474, 1.6271505915615332, 1654.904761904762, 2662.6826680016134),
       'sum_shortest_distance_int_0.7_0.3': (
       7.0, 1.6733200530681511, 1357.3809523809523, 1948.7939982509818),
       'sum_shortest_distance_int_0.8_0.2': (
       7.238095238095238, 1.7579750255553093, 1392.142857142857, 1867.7822754730887),
       'sum_shortest_distance_int_0.9_0.1': (
       7.380952380952381, 1.8296499795368095, 1407.0, 2060.215280013232)}

if __name__ == "__main__":
    for key, value in var.items():
        rounded_tuple = tuple(round(x, 3) for x in value)
        print(f"{key}: {rounded_tuple}")