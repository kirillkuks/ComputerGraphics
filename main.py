from matching_algorithm import MatchingAlgorithm

if __name__ == '__main__':
    f_1 = [[121, 27], [220, 45], [202, 143], [104, 126]]
    f_2 = [[0, 0], [0, 1], [1, 1], [1, 0]]

    s_1 = [[164, 79], [191, 132], [244, 106], [217, 51]]
    s_2 = [[0, 0], [0, 1], [1, 1], [1, 0]]

    t_1 = [[121, 120], [158, 154], [125, 191], [88, 158]]
    t_2 = [[0, 0], [0, 1], [1, 1], [1, 0]]

    fr_1 = [[1, 2], [2, 4], [3, 2], [5, 4], [6, 2], [5, 1], [2, 1]]
    fr_2 = [[-7, 1], [-3, 3], [-7, 7], [-3, 9], [-1, 7], [-1, 1], [-3, -1]]

    fv_1 = [[0, 0], [1, 0], [1, 1]]
    fv_2 = [[270, 170], [180, 170], [180, 80]]

    ego_1 = [164, 79], [191, 132], [245, 105], [217, 51]
    ego_2 = [0, 0], [0, 1], [1, 1], [1, 0]

    ma = MatchingAlgorithm()

    print(ma.match(f_1, f_2))
    print(ma.match(f_2, f_1))

    print(ma.match(s_1, s_2))
    print(ma.match(s_2, s_1))

    print(ma.match(t_1, t_2))
    print(ma.match(t_2, t_1))

    print(ma.match(fr_1, fr_2))
    print(ma.match(fr_2, fr_1))

    print(ma.match(fv_1, fv_2))
    print(ma.match(fv_2, fv_1))

    print(ma.match(ego_1, ego_2))
    print(ma.match(ego_2, ego_1))


