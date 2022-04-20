from __future__ import annotations

import numpy as np


class Figure:
    def __init__(self, points: np.ndarray) -> None:
        self.points = np.copy(points)

    def vertices_num(self) -> int:
        return len(self.points)

    def calculate_edges(self) -> np.ndarray:
        edges = []
        size = self.vertices_num()

        for i in range(size):
            edges.append(np.linalg.norm(self.points[i] - self.points[(i + 1) % size], ord=2))

        return np.array(edges)

    def get_vertices(self) -> np.ndarray:
        return np.copy(self.points)        
