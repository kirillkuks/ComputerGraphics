import cv2 as cv
import argparse
import numpy as np
import matplotlib.pyplot as plt


from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
from skimage.morphology import binary_opening, binary_closing
from skimage.measure import regionprops
from skimage.measure import label as sk_measure_label

from line import Line
from figure import Figure
from matching_algorithm import MatchingAlgorithm
from input_reader import InputReader


class ShapeFinder:
    def __init__(self) -> None:
        pass

    def find(self, image_name: str) -> None:
        image = cv.imread(image_name, cv.IMREAD_GRAYSCALE)
        
        closed = binary_closing(image)

        figures = []

        for closed, coords in self.get_all_components(closed):
            is_need, edged = self.need_canny(closed)

            closed = edged if is_need else closed

            h, theta, d = hough_line(closed)

            lines = []

            for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
                x0 = (dist - 0 * np.sin(angle)) / np.cos(angle)
                x1 = (dist - image.shape[0] * np.sin(angle)) / np.cos(angle)

                lines.append([dist, angle])

            dots = []
            dots_per_line = []
            lines_func = []

            for i in range(len(lines)):
                dots_on_line = []
                d1, a1 = lines[i][0], lines[i][1]
                line1 = Line(d1, a1)

                lines_func.append(line1)

                for j in range(len(lines)):

                    if i != j:
                        d2, a2 = lines[j][0], lines[j][1]

                        A = np.array([
                            [np.cos(a1), np.sin(a1)],
                            [np.cos(a2), np.sin(a2)]
                        ])
                        b = np.array([
                            [d1],
                            [d2]
                        ])

                        line2 = Line(d2, a2)

                        dt1 = line1.used_pixels(closed)
                        dt2 = line2.used_pixels(closed)

                        if self.line_intersection(dt1, dt2):

                            if np.linalg.matrix_rank(A) == 2:
                                x, y = np.linalg.solve(A, b)
                                x, y = int(np.round(x)), int(np.round(y))

                                if x > 0 and y > 0 and x < image.shape[1] and y < image.shape[0]:
                                    dots.append((x, y))

                                    dots_on_line.append((x, y))


                dots_per_line.append(dots_on_line)

            extremes = []

            for line, dots in zip(lines_func, dots_per_line):
                if len(dots) >= 2:
                    extremes.append(line.get_extreme_points(dots))

            dots = self.dots_on_contour(coords, dots)

            figure = self.find_circle(extremes)
            
            if figure is not None:
                for dot in figure:
                    pass

                figures.append(Figure(figure))

        return figures

    def find_circle(self, lines: np.ndarray) -> np.ndarray:
        for i in range(len(lines)):
            is_figure, figure = self.find_figure(lines, i)

            if is_figure:
                return figure

        return None

    def find_figure(self, lines: np.ndarray, start_ind: int = 0):
        pivot = lines[start_ind][0]
        end = lines[start_ind][1]

        lines_inds = [start_ind]
        figure = [pivot]

        next = True

        while next:
            next = False

            for i, line in enumerate(lines):
                if i not in lines_inds:
                    if self.in_line(line, pivot):
                        pivot = self.other(line, pivot)
                        
                        lines_inds.append(i)
                        figure.append(pivot)

                        next = True

        return figure[-1][0] == end[0] and figure[-1][1] == end[1], np.array(figure)

    def in_line(self, line: np.ndarray, point: np.ndarray) -> bool:
        assert len(point) == 2
        assert len(line) == 2

        return (point[0] == line[0][0] and point[1] == line[0][1]) or (point[0] == line[1][0] and point[1] == line[1][1])

    def other(self, line: np.ndarray, point: np.ndarray) -> np.ndarray:
        assert point in line

        return line[0] if point[0] == line[1][0] and point[1] == line[1][1] else line[1]

    def delete_noise(self, arr: np.ndarray, noise_rad: int) -> None:
        assert noise_rad > 0
        
        i = 0

        while i < len(arr):
            if arr[i] == True:
                k = i + 1

                while k < len(arr) and arr[k] == True:
                    k += 1

                if k - i < noise_rad:
                    for j in range(i, k):
                        arr[j] = False

                i = k
            else:
                i += 1        

    def line_intersection(self, dots1, dots2) -> bool:
        for dot1 in dots1:
            for dot2 in dots2:
                if dot1[0] in self.neighborhood(dot2[0], 2):
                    if dot1[1] in self.neighborhood(dot2[1], 2):
                        return True

        return False

    def neighborhood(self, center: int, rad: int) -> np.ndarray:
        assert rad > 0

        return np.array([center - rad + k for k in range(2 * rad + 1)])

    def dots_on_contour(self, coords, dots):
        intersection = []

        for dot in dots:
            for coord in coords:
                if dot[0] in [coord[1] - 1, coord[1], coord[1] + 1] and dot[1] in [coord[0] - 1, coord[0], coord[0] + 1]:
                    intersection.append(dot)

        return intersection

    def get_all_components(self, mask: np.ndarray):
        labels = sk_measure_label(mask)
        props = regionprops(labels)
        areas = np.array([np.array([i, prop.area, prop.coords]) for i, prop in enumerate(props) if prop.area > 10], dtype=object)

        for i in range(len(areas)):
            yield labels == (areas[i][0] + 1), areas[i][2]

    def get_largest_component(self, mask: np.ndarray):
        labels = sk_measure_label(mask)
        props = regionprops(labels)
        areas = np.array([np.array([i, prop.area, prop.coords]) for i, prop in enumerate(props) if prop.area > 10], dtype=object)

        largest_comp_id = np.array(areas[:, 1]).argmax()

        ind = largest_comp_id

        return labels == (areas[ind][0] + 1), areas[ind][2]

    def need_canny(self, image: np.ndarray) -> bool:
        edged_image = canny(image, sigma=1.5, low_threshold=0.1)

        return np.sum(edged_image) < np.sum(image), edged_image


def parse_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-s', help='input file')
    args_parser.add_argument('-i', help='input image')

    args = args_parser.parse_args()

    assert args.s is not None
    assert args.i is not None

    return args.s, args.i


def main():
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

    input_file, image = parse_args()

    input_reader = InputReader(input_file)
    input_figures = input_reader.read()

    shape_finder = ShapeFinder()
    figures = shape_finder.find(image)

    match = MatchingAlgorithm(10)

    answer = []

    for figure in figures:
        founded = False

        for i, input_figure in enumerate(input_figures):
            res, shift_x, shift_y, scale, rotate = match.match(input_figure.get_vertices(), figure.get_vertices())

            if res == True:
                answer.append([i, shift_x, shift_y, scale, rotate])
                founded = True

            if founded:
                break


    print(len(answer))

    for line in answer:
        print(f'{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}')

    return


if __name__ == '__main__':
    main()
