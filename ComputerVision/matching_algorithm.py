import math


class MatchingAlgorithm:
    def __init__(self, eps_coeff=50) -> None:
        self.eps_coeff = eps_coeff
        pass

    def match(self, origin_poly: [], searched_poly: []):
        if len(origin_poly) != len(searched_poly):
            return False, 0.0, 0.0, 0.0, 0.0

        for poly in [searched_poly, list(reversed(searched_poly))]:

            eps, f_longest_sides = self._find_longest_sides(origin_poly)
            _, s_longest_sides = self._find_longest_sides(poly)

            if len(f_longest_sides) != len(s_longest_sides):
                return False, 0.0, 0.0, 0.0, 0.0

            for f_longest_side in f_longest_sides:
                for s_longest_side in s_longest_sides:
                    coeff = self._dist(origin_poly[f_longest_side[0]], origin_poly[f_longest_side[1]]) / \
                            self._dist(poly[s_longest_side[0]], poly[s_longest_side[1]])

                    if s_longest_side[0] != f_longest_side[0]:
                        shift = s_longest_side[0] - f_longest_side[0]
                        if shift < 0:
                            shift = len(origin_poly) + shift
                        elif shift >= len(origin_poly):
                            shift = shift - len(origin_poly)
                        temp_poly = self._recalc_indexes(poly, shift)
                    else:
                        temp_poly = poly

                    index = f_longest_side[0]

                    answer_dist = [x - y for x, y in zip(origin_poly[0], temp_poly[0])]
                    dist = [x - y for x, y in zip(origin_poly[index], temp_poly[index])]

                    temp_poly = list(map(lambda point: [point[0] + dist[0], point[1] + dist[1]], temp_poly))

                    temp_poly = self._resize_by_point(temp_poly, index, coeff)

                    f_vector = [x - y for x, y in zip(origin_poly[f_longest_side[1]], origin_poly[index])]
                    s_vector = [x - y for x, y in zip(temp_poly[f_longest_side[1]], temp_poly[index])]

                    angle = self._find_angle(s_vector, f_vector)

                    temp_poly1 = self._rotate_by_angle(temp_poly, index, angle)
                    temp_poly2 = self._rotate_by_angle(temp_poly, index, -angle)

                    miss_flag = False

                    for j in range(len(temp_poly1)):
                        if self._dist(temp_poly1[j], origin_poly[j]) > eps:
                            miss_flag = True
                            break
                    if not miss_flag:
                        return True, answer_dist[0], answer_dist[1], coeff, -math.degrees(angle)

                    miss_flag = False

                    for j in range(len(temp_poly2)):
                        if self._dist(temp_poly2[j], origin_poly[j]) > eps:
                            miss_flag = True
                            break
                    if not miss_flag:
                        return True, answer_dist[0], answer_dist[1], coeff, -math.degrees(-angle)

        return False, 0.0, 0.0, 0.0, 0.0

    def _find_longest_sides(self, poly: []):
        max_dist = 0.0
        eps = -math.inf
        indexes = []
        for i in range(len(poly)):
            if i == len(poly) - 1:
                j = 0
            else:
                j = i + 1

            dist = self._dist(poly[i], poly[j])

            if dist / self.eps_coeff > eps:
                eps = dist / self.eps_coeff

            if abs(max_dist - dist) < eps:
                indexes.append([i, j])
            elif dist > max_dist:
                indexes.clear()
                max_dist = dist
                indexes.append([i, j])
        return eps, indexes

    @staticmethod
    def _dist(f_point: [], s_point: []) -> float:
        return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(f_point, s_point)))

    @staticmethod
    def _recalc_indexes(poly: [], index) -> []:
        new_poly = []
        for i in range(index, len(poly)):
            new_poly.append(poly[i])
        for i in range(index):
            new_poly.append(poly[i])
        return new_poly

    @staticmethod
    def _resize_by_point(poly: [], index, coeff) -> []:
        resized_poly = []
        for i in range(len(poly)):
            if i == index:
                resized_poly.append(poly[i])
                continue

            dist = [x - y for x, y in zip(poly[i], poly[index])]

            dist = [x * coeff for x in dist]

            resized_poly.append([poly[index][0] + dist[0], poly[index][1] + dist[1]])
        return resized_poly

    @staticmethod
    def _rotate(origin: [], point: [], angle) -> []:
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return [qx, qy]

    @staticmethod
    def _find_angle(f_vector, s_vector) -> float:
        ma = math.sqrt(f_vector[0] ** 2 + f_vector[1] ** 2)
        mb = math.sqrt(s_vector[0] ** 2 + s_vector[1] ** 2)
        sc = f_vector[0] * s_vector[0] + f_vector[1] * s_vector[1]
        return math.acos(sc / ma / mb)

    @staticmethod
    def _rotate_by_angle(poly: [], index, angle) -> []:
        rotated_poly = []
        for i in range(len(poly)):
            if i == index:
                rotated_poly.append(poly[i])
                continue

            rotated_poly.append(MatchingAlgorithm._rotate(poly[index], poly[i], angle))
        return rotated_poly
