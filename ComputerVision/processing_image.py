import math
from copy import copy

import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt

intent = 5


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_x(self) -> int: return self.x

    def get_y(self) -> int: return self.y

    @staticmethod
    def same_points(point1, point2) -> bool:
        if math.fabs(point1.get_x() - point2.get_x()) < 10e-2 and math.fabs(point1.get_y() - point2.get_y()) < 10e-2:
            return True
        return False


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def get_point1(self) -> Point: return self.point1

    def get_point2(self) -> Point: return self.point2

    def point1_as_tuple(self) -> tuple: return int(self.point1.get_x()), int(self.point1.get_y())

    def point2_as_tuple(self) -> tuple: return int(self.point2.get_x()), int(self.point2.get_y())

    def point_in_line(self, point: Point) -> bool:
        x_max = max(self.point1.get_x(), self.point2.get_x())
        x_min = min(self.point1.get_x(), self.point2.get_x())
        y_max = max(self.point1.get_y(), self.point2.get_y())
        y_min = min(self.point1.get_y(), self.point2.get_y())

        if math.fabs(self.point1.get_x() - self.point2.get_x()) < 10e-3:
            return (math.fabs(x_min - int(point.get_x())) < intent and y_min - intent < point.get_y() < y_max + intent)

        a = (self.point1.get_y() - self.point2.get_y()) / (self.point1.get_x() - self.point2.get_x())
        b = self.point1.get_y() - a * self.point1.get_x()

        if x_min - intent < point.get_x() < x_max + intent and y_min - intent < point.get_y() < y_max + intent and \
                math.fabs(point.get_y() - a * point.get_x() - b) < intent:
            return True

        return False

    def zero_div(self, other):
        if math.fabs(other.get_point1().get_x() - other.get_point2().get_x()) < 10e-2:
            return None

        a = (other.get_point1().get_y() - other.get_point2().get_y()) / \
            (other.get_point1().get_x() - other.get_point2().get_x())
        b = other.get_point1().get_y() - a * other.get_point1().get_x()
        y = a * self.point1.get_x() + b
        y_min = min(self.point1.get_y(), self.point2.get_y())
        y_max = max(self.point1.get_y(), self.point2.get_y())
        x_min = min(other.get_point1().get_x(), other.get_point2().get_x())
        x_max = max(other.get_point1().get_x(), other.get_point2().get_x())
        if y_min - intent < y < y_max + intent and \
                x_min - intent < self.point1.get_x() < x_max:
            return Point(self.point1.get_x(), y)
        else:
            return None

    @staticmethod
    def intersect(line1, line2):
        if math.fabs(line1.get_point1().get_x() - line1.get_point2().get_x()) < 10e-2:
            return line1.zero_div(line2)
        if math.fabs(line2.get_point1().get_x() - line2.get_point2().get_x()) < 10e-2:
            return line2.zero_div(line1)


        point1 = line1.get_point1()
        point2 = line1.get_point2()

        a = (point1.get_y() - point2.get_y()) / (point1.get_x() - point2.get_x())
        b = point1.get_y() - a * point1.get_x()

        point1 = line2.get_point1()
        point2 = line2.get_point2()
        a_ = (point1.get_y() - point2.get_y()) / (point1.get_x() - point2.get_x())
        b_ = point1.get_y() - a_ * point1.get_x()

        if math.fabs(a - a_) < 10e-3:
            return None

        x = (b_ - b) / (a - a_)
        y = a * x + b

        point = Point(x, y)

        if line1.point_in_line(point) and line2.point_in_line(point): return point
        return None


class Figure:
    def __init__(self, ps: list, lines: list):
        lp = []
        for index, line in enumerate(lines):
            lp.append(set())
            for point in ps:
                if line.point_in_line(point):
                    lp[index].add(point)

        self.lines = []
        for points in lp:
            if len(points) > 1:
                x_sort = sorted(points, key=Point.get_x)
                if math.fabs(x_sort[0].get_x() - x_sort[-1].get_x()) > 0.01:
                    point1 = x_sort[0]
                    point2 = x_sort[-1]
                else:
                    y_sort = sorted(points, key=Point.get_y)
                    if math.fabs(y_sort[0].get_y() - y_sort[-1].get_y()) < 0.01: continue
                    point1 = y_sort[0]
                    point2 = y_sort[-1]
                self.lines.append(Line(point1, point2))
        self.lines = np.array(self.lines)

    def get_lines(self) -> np.ndarray: return self.lines

    def is_valide(self) -> bool:
        flag = False
        while not flag and self.lines.shape[0] > 2:
            checks = [[False, False] for i in range(self.lines.shape[0])]
            for index1, line1 in enumerate(self.lines):
                point1 = line1.get_point1()
                point2 = line1.get_point2()
                for index2, line2 in enumerate(self.lines):
                    if index1 != index2:
                        if line2.point_in_line(point1):
                            checks[index1][0] = True
                        if line2.point_in_line(point2):
                            checks[index1][1] = True

            flag = True
            lines = []
            for index, check in enumerate(checks):
                if check[0] and check[1]:
                    lines.append(self.lines[index])
                else:
                    flag = False
            self.lines = np.array(lines)

        return flag


def get_intersect_points(path: str) -> np.ndarray:
    image = cv2.imread(path, cv2.CV_8UC1)
    plt.imshow(image)

    hough_lines = cv2.HoughLinesP(image, .5, np.pi/180, 15, maxLineGap=5, minLineLength=20)[:, 0, :]
    lines = []
    for x1, y1, x2, y2 in hough_lines:
        point1 = Point(x1, y1)
        point2 = Point(x2, y2)
        lines.append(Line(point1, point2))

    points = []
    figures = []
    for i, line in enumerate(lines):
        n = [index for index, num in enumerate(figures) if i in num]
        if len(n) == 0:
            n = len(figures)
            figures.append([i])
        else:
            n = n[0]
        for j in range(0, len(lines)):
            point = Line.intersect(lines[i], lines[j])
            if point is not None:
                flag = True
                for p in points:
                    if Point.same_points(point, p):
                        flag = False
                        break
                if flag: points.append(point)
                figures[n].append(j)

    result_figs = copy(figures)
    for i in range(len(figures)):
        for j in range(i + 1, len(figures)):
            if set(figures[i]) <= set(figures[j]):
                result_figs.remove(figures[i])
    figures = result_figs

    figs = []
    for figure in figures:
        if len(figure) > 2:
            print(len(set(figure)))
            figs.append(Figure(points, [lines[i] for i in set(figure)]))
            # img = np.zeros(image.shape, dtype=np.uint8)
            # for line in [lines[i] for i in set(figure)]:
            #     cv2.line(img, line.point1_as_tuple(), line.point2_as_tuple(), 255)
            # plt.imshow(img)
            # plt.show()

    figures = []
    for figure in figs:
        if figure.is_valide():
            figures.append(figure)
            img = np.zeros(image.shape, dtype=np.uint8)
            for line in figure.get_lines():
                cv2.line(img, line.point1_as_tuple(), line.point2_as_tuple(), 255)
            plt.imshow(img)
            plt.show()

    return np.array(figures)
