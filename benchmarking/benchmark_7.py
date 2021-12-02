var = {'minkowski': (7.458333333333333, 1.7687914485336584, 1751.9166666666667, 3437.309285355103),
       'minkowski_int': (7.458333333333333, 1.7687914485336584, 2422.9583333333335, 4388.978354718602),
       'euclid': (7.5, 1.8177865182927715, 1763.625, 3466.9158930932563),
       'euclid_int': (7.583333333333333, 1.7916877315917057, 1740.5833333333333, 2461.147009312787),
       'manhattan': (7.625, 1.8838558977475588, 2377.4583333333335, 4597.952086472058),
       'chebyshev': (7.541666666666667, 1.7440374613713625, 1661.375, 2453.728906972619),
       'shortest_distance': (6.958333333333333, 1.6279933411536363, 2730.5833333333335, 4509.822187921234),
       'shortest_distance_int': (6.958333333333333, 1.6279933411536363, 3147.75, 5273.598962922676),
       'min_shortest_distance': (6.958333333333333, 1.6279933411536363, 3147.75, 5273.598962922676),
       'sum_shortest_distance': (7.916666666666667, 2.041241452319315, 781.8333333333334, 1432.432278288945),
       'sum_shortest_distance_0.1_0.9': (6.916666666666667, 1.6396358733271998, 1741.7083333333333, 3726.240738554967),
       'sum_shortest_distance_0.2_0.8': (6.916666666666667, 1.6396358733271998, 1656.5416666666667, 3550.092086731746),
       'sum_shortest_distance_0.3_0.7': (6.916666666666667, 1.6396358733271998, 1485.5833333333333, 3238.883945149151),
       'sum_shortest_distance_0.4_0.6': (6.916666666666667, 1.6396358733271998, 1469.2916666666667, 3250.015698680034),
       'sum_shortest_distance_0.5_0.5': (7.0, 1.6151457061744965, 1376.3333333333333, 2894.7388808674605),
       'sum_shortest_distance_0.6_0.4': (7.166666666666667, 1.7110044511584586, 1459.9166666666667, 2945.3865903590086),
       'sum_shortest_distance_0.7_0.3': (
       7.166666666666667, 1.7110044511584586, 1358.9166666666667, 2526.370053045978),
       'sum_shortest_distance_0.8_0.2': (
       7.208333333333333, 1.7440374613713625, 1458.4166666666667, 2626.1379465848236),
       'sum_shortest_distance_0.9_0.1': (
       7.333333333333333, 1.7362294645648624, 1509.0, 2841.6158752739075), 'sum_shortest_distance_int_0.1_0.9': (
    6.958333333333333, 1.6279933411536363, 3107.7083333333335, 5190.841705049776),
       'sum_shortest_distance_int_0.2_0.8': (
       6.958333333333333, 1.6279933411536363, 2941.9166666666665, 4878.536985940396),
       'sum_shortest_distance_int_0.3_0.7': (
       6.958333333333333, 1.6279933411536363, 2517.5833333333335, 4298.754035022612),
       'sum_shortest_distance_int_0.4_0.6': (6.958333333333333, 1.6279933411536363, 2187.5, 3978.2847953664),
       'sum_shortest_distance_int_0.5_0.5': (7.0, 1.6151457061744965, 1725.3333333333333, 3031.2921002604567),
       'sum_shortest_distance_int_0.6_0.4': (7.125, 1.701980943029264, 2386.7916666666665, 4801.462639284958),
       'sum_shortest_distance_int_0.7_0.3': (
       7.25, 1.7507762253652943, 2178.9583333333335, 4183.137354740242),
       'sum_shortest_distance_int_0.8_0.2': (
       7.291666666666667, 1.6544844636864107, 2329.8333333333335, 4326.858009212234),
       'sum_shortest_distance_int_0.9_0.1': (
       7.416666666666667, 1.7672544824662637, 1920.5833333333333, 3112.5212891420224)}

if __name__ == "__main__":
    for key, value in var.items():
        rounded_tuple = tuple(round(x, 3) for x in value)
        print(f"{key}: {rounded_tuple}")
