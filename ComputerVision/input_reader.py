import numpy as np

from figure import Figure


class InputReader:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read(self) -> np.ndarray:
        figures_num = 0
        figures = []
        
        with open(self.filename) as f:
            figures_num = int(f.readline())

            for _ in range(figures_num):
                vertices = f.readline().replace(' ', '').split(',')
                
                figures.append(self._group_vertices(vertices))

        return figures

    def _group_vertices(self, vertices: np.ndarray) -> Figure:
        assert len(vertices) % 2 == 0

        size = len(vertices) // 2
        group = np.array([[int(vertices[2 * i]), int(vertices[2 * i + 1])] for i in range(size)])

        return Figure(group)
