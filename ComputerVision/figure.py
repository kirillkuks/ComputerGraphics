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

    def match(self, figure: Figure) -> bool:
        if self.vertices_num() != figure.vertices_num():
            return False

        edges = self.calculate_edges()
        fig_edges = figure.calculate_edges()

        relation_coef = edges[0] / fig_edges[0]

        is_matched = False
        i = 0

        while not is_matched:
            i += 1
            is_matched = True

            print(f'coef = {relation_coef}')
            print(f'edges = {edges}')
            print(f'fig edges = {fig_edges}')
            print('##########################')

            for e1, e2 in zip(edges, fig_edges):

                if np.abs(e1 / e2 - relation_coef) > 1e-2:
                    is_matched = False

                    self.shift_vertices()
                    edges = self.calculate_edges()
                    relation_coef = edges[0] / fig_edges[0]

        print(':-)')
        print(self.points)
        print(f'i = {i}')

    def shift_vertices(self) -> None:
        print(f'before = {self.points}')
        self.points =np.roll(self.points, 1, axis=0)
        print(f'after = {self.points}')
        
