import math


def find_longest_sides(poly: [], eps):
    max_dist = 0.0
    indexes = []
    for i in range(len(poly)):
        if i == len(poly) - 1:
            j = 0
        else:
            j = i + 1

        dist = math.dist(poly[i], poly[j])

        if abs(max_dist - dist) < eps:
            indexes.append([i, j])
        elif dist > max_dist:
            indexes.clear()
            max_dist = dist
            indexes.append([i, j])
    return indexes


def recalc_indexes(poly: [], index):
    new_poly = []
    for i in range (index, len(poly)):
        new_poly.append(poly[i])
    for i in range(index):
        new_poly.append(poly[i])
    return new_poly


def resize_by_point(poly: [], index, coeff):
    resized_poly = []
    for i in range(len(poly)):
        if i == index:
            resized_poly.append(poly[i])
            continue

        dist = [x - y for x, y in zip(poly[i], poly[index])]

        dist = [x * coeff for x in dist]

        resized_poly.append([poly[index][0] + dist[0], poly[index][1] + dist[1]])
    return resized_poly


def rotate(origin: [], point: [], angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return [qx, qy]


def find_angle(f_vector, s_vector):
    ma = math.sqrt(f_vector[0] ** 2 + f_vector[1] ** 2)
    mb = math.sqrt(s_vector[0] ** 2 + s_vector[1] ** 2)
    sc = f_vector[0] * s_vector[0] + f_vector[1] * s_vector[1]
    return math.acos(sc / ma / mb)


def rotate_by_angle(poly: [], index,  angle):
    rotated_poly = []
    for i in range(len(poly)):
        if i == index:
            rotated_poly.append(poly[i])
            continue

        rotated_poly.append(rotate(poly[index], poly[i], angle))
    return rotated_poly


def calc_shift(f_poly: [], s_poly: []):
    f_sum_x = 0
    s_sum_x = 0
    f_sum_y = 0
    s_sum_y = 0
    m = len(f_poly)
    for j in range(m):
        f_sum_x += f_poly[j][0]
        f_sum_y += f_poly[j][1]
        s_sum_x += s_poly[j][0]
        s_sum_y += s_poly[j][1]
    f_sum_x /= m
    s_sum_x /= m
    f_sum_y /= m
    s_sum_y /= m
    return f_sum_x - s_sum_x, f_sum_y - s_sum_y


def match_alg(f_poly: [], s_poly: [],  eps=1e-7):

    if len(s_poly) != len(f_poly):
        return False, 0.0, 0.0, 0.0, 0.0

    f_longest_sides = find_longest_sides(s_poly, eps)
    s_longest_sides = find_longest_sides(f_poly, eps)

    if len(f_longest_sides) != len(s_longest_sides):
        return False, 0.0, 0.0, 0.0, 0.0

    for f_longest_side in f_longest_sides:
        for s_longest_side in s_longest_sides:
            coeff = math.dist(s_poly[f_longest_side[0]], s_poly[f_longest_side[1]]) / \
                    math.dist(f_poly[s_longest_side[0]], f_poly[s_longest_side[1]])
            for i in range(2):
                if s_longest_side[i] != f_longest_side[0]:
                    shift = s_longest_side[i] - f_longest_side[0]
                    if shift < 0:
                        shift = len(s_poly) + shift
                    elif shift >= len(s_poly):
                        shift = shift - len(s_poly)
                    temp_poly = recalc_indexes(f_poly, shift)
                else:
                    temp_poly = f_poly

                index = f_longest_side[0]

                dist = [x - y for x, y in zip(s_poly[index], temp_poly[index])]

                temp_poly = list(map(lambda point: [point[0] + dist[0], point[1] + dist[1]], temp_poly))

                temp_poly = resize_by_point(temp_poly, index, coeff)

                f_vector = [x - y for x, y in zip(s_poly[f_longest_side[1]], s_poly[index])]
                if i == 0:
                    s_vector = [x - y for x, y in zip(temp_poly[index + 1], temp_poly[index])]
                else:
                    s_vector = [x - y for x, y in zip(temp_poly[len(temp_poly) - 1], temp_poly[index])]

                angle = find_angle(s_vector, f_vector)

                temp_poly1 = rotate_by_angle(temp_poly, index, angle)
                temp_poly2 = rotate_by_angle(temp_poly, index, -angle)

                miss_flag = False

                for j in range(len(temp_poly1)):
                    if math.dist(temp_poly1[j], s_poly[j]) > eps:
                        miss_flag = True
                        break
                if miss_flag:
                    return True, dist[0], dist[1], coeff, -math.degrees(angle)
                    #return True, calc_shift(f_poly, s_poly), coeff, -math.degrees(angle)

                miss_flag = False

                for j in range(len(temp_poly2)):
                    if math.dist(temp_poly2[j], s_poly[j]) > eps:
                        miss_flag = True
                        break
                if miss_flag:
                    return True, dist[0], dist[1], coeff, -math.degrees(-angle)
                    #return True, calc_shift(f_poly, s_poly), coeff, -math.degrees(-angle)
    return False
