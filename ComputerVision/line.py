import numpy as np


class Line:
    def __init__(self, dist: float, angle: float) -> None:
        self.dist: float = dist
        self.angle: float = angle

    def calculate_by_x(self, x: float) -> None:
        return (self.dist - x * np.cos(self.angle)) / np.sin(self.angle)

    def calculate_by_y(self, y: float) -> None:
        return (self.dist - y * np.sin(self.angle)) / np.cos(self.angle)

    def get_extreme_points(self, points: np.ndarray) -> np.ndarray:
        min_val, max_val = np.inf, -np.inf
        min_ind, max_ind = -1, -1

        axis_ind = 1 if - np.pi / 4 < self.angle < np.pi / 4 else 0

        for i, point in enumerate(points):
            if point[axis_ind] > max_val:
                max_val = point[axis_ind]
                max_ind = i

            if point[axis_ind] < min_val:
                min_val = point[axis_ind]
                min_ind = i

        extreme = np.array([points[min_ind], points[max_ind]])
        deleted = np.delete(points, [min_ind, max_ind])

        return extreme

    def used_pixels(self, image: np.ndarray) -> np.ndarray:
        is_line = []

        if - np.pi / 4 < self.angle < np.pi / 4:
            y = np.array([i for i in range(image.shape[0])])
            x = np.array([int(np.round(self.calculate_by_y(y_k))) for y_k in y])

            for x_k, y_k in zip(x, y):
                is_line.append(False)

                if x_k > 0 and x_k < image.shape[1] - 1:
                    if image[y_k][x_k] > 0 or image[y_k][x_k - 1] > 0 or image[y_k][x_k + 1] > 0:
                        is_line[-1] = True  

        else:
            x = np.array([i for i in range(image.shape[1])])
            y = np.array([int(np.round(self.calculate_by_x(x_k))) for x_k in x])

            for x_k, y_k in zip(x, y):
                is_line.append(False)
                    
                if y_k > 0 and y_k < image.shape[0] - 1:
                    if image[y_k][x_k] > 0 or image[y_k - 1][x_k] > 0 or image[y_k + 1][x_k] > 0:
                        is_line[-1] = True

        self._delete_noise(is_line, 3)

        dots = []

        for k, (x_k, y_k) in enumerate(zip(x, y)):
            if is_line[k] == True:
                dots.append((x_k, y_k))

        return dots

    def _delete_noise(self, arr: np.ndarray, noise_rad: int) -> None:
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
