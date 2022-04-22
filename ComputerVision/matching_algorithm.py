import math
import numpy as np


class MatchingAlgorithm:
    def __init__(self, eps_coeff=10) -> None:
        self.eps_coeff = eps_coeff

    def match(self, origin_poly, searched_poly):
        if len(origin_poly) != len(searched_poly):
            return False, 0, 0, 0, 0

        for sp in [searched_poly, list(reversed(searched_poly))]:

            eps, sp_longest_sides = self._find_longest_sides(sp)
            _, op_longest_sides = self._find_longest_sides(origin_poly)

            if len(sp_longest_sides) != len(op_longest_sides):
                return False, 0, 0, 0, 0

            for sp_longest_side in sp_longest_sides:
                for op_longest_side in op_longest_sides:
                    coeff = self._dist(sp[sp_longest_side[0]], sp[sp_longest_side[1]]) / \
                            self._dist(origin_poly[op_longest_side[0]], origin_poly[op_longest_side[1]])

                    if sp_longest_side[0] != op_longest_side[0]:
                        shift = sp_longest_side[0] - op_longest_side[0]
                        if shift < 0:
                            shift = len(sp) + shift
                        elif shift >= len(sp):
                            shift = shift - len(sp)
                        tmp_sp = self._recalc_indexes(sp, shift)
                    else:
                        tmp_sp = sp

                    index = op_longest_side[0]

                    tmp_op = origin_poly

                    answer_dist = [x - y for x, y in zip(tmp_sp[0], tmp_op[0])]
                    dist = [x - y for x, y in zip(tmp_sp[index], tmp_op[index])]

                    tmp_op = list(map(lambda point: [point[0] + dist[0], point[1] + dist[1]], tmp_op))

                    tmp_op = self._resize_by_point(tmp_op, index, coeff)

                    f_vector = [x - y for x, y in zip(tmp_sp[op_longest_side[1]], tmp_sp[index])]
                    s_vector = [x - y for x, y in zip(tmp_op[op_longest_side[1]], tmp_op[index])]

                    angle = self._find_angle(s_vector, f_vector)

                    tmp_op_poly1 = self._rotate_by_angle(tmp_op, index, angle)
                    tmp_op_poly2 = self._rotate_by_angle(tmp_op, index, -angle)

                    for poly, t_angle in zip([tmp_op_poly1, tmp_op_poly2], [angle, -angle]):
                        miss_flag = False

                        for j in range(len(poly)):
                            if self._dist(poly[j], tmp_sp[j]) > eps:
                                miss_flag = True
                                break
                        if not miss_flag:
                            return True, self._int_r(answer_dist[0]), self._int_r(answer_dist[1]), self._int_r(coeff), \
                                   self._int_r(np.degrees(t_angle))

        return False, 0, 0, 0, 0

    def _find_longest_sides(self, poly):
        max_dist = 0.0
        eps = -np.inf
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
    def _dist(f_point, s_point) -> float:
        return np.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(f_point, s_point)))

    @staticmethod
    def _int_r(num):
        num = int(num + (0.5 if num > 0 else -0.5))
        return num

    @staticmethod
    def _recalc_indexes(poly, index) -> list:
        new_poly = []
        for i in range(index, len(poly)):
            new_poly.append(poly[i])
        for i in range(index):
            new_poly.append(poly[i])
        return new_poly

    @staticmethod
    def _resize_by_point(poly, index, coeff) -> list:
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
    def _rotate(origin, point, angle) -> list:
        ox, oy = origin
        px, py = point

        qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
        qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
        return [qx, qy]

    @staticmethod
    def _find_angle(f_vector, s_vector) -> float:
        ma = np.sqrt(f_vector[0] ** 2 + f_vector[1] ** 2)
        mb = np.sqrt(s_vector[0] ** 2 + s_vector[1] ** 2)
        sc = f_vector[0] * s_vector[0] + f_vector[1] * s_vector[1]

        res = sc / (ma * mb)

        if res < -1:
            return np.pi
        elif res > 1:
            return 0
        else:
            return np.arccos(res)

    @staticmethod
    def _rotate_by_angle(poly, index, angle) -> list:
        rotated_poly = []
        for i in range(len(poly)):
            if i == index:
                rotated_poly.append(poly[i])
                continue

            rotated_poly.append(MatchingAlgorithm._rotate(poly[index], poly[i], angle))
        return rotated_poly
