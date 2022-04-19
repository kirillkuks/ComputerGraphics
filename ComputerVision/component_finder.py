import numpy as np

from skimage.measure import regionprops
from skimage.measure import label as sk_measure_label


class ComponentFinder:
    class ComponentInfo:
        def __init__(self, ind: int, area: float, coords: np.ndarray) -> None:
            self.ind = ind
            self.area = area
            self.coords = np.copy(coords)

        def get_ind(self) -> int:
            return self.ind

        def get_area(self) -> float:
            return self.area

        def get_coords(self) -> np.ndarray:
            return self.coords


    def __init__(self, mask: np.ndarray) -> None:
        self.mask = np.copy(mask)

        labels = sk_measure_label(self.mask)
        props = regionprops(labels)

        self.infos = np.array([ComponentFinder.ComponentInfo(i, prop.area, prop.coords) for i, prop in enumerate(props) if prop.area > 10])

    def get_largest_component(self):
        labels = sk_measure_label(self.mask) # разбиение маски на компоненты связности
        props = regionprops(labels) # нахождение свойств каждой области (положение центра, площадь, bbox, интервал интенсивностей и т.д.)
        areas = np.array([np.array([i, prop.area, prop.coords]) for i, prop in enumerate(props) if prop.area > 10], dtype=object) # нас интересуют площади компонент связности

        # print("Значения площади для каждой компоненты связности: {}".format(areas))
        largest_comp_id = np.array(areas[:, 1]).argmax() # находим номер компоненты с максимальной площадью

        ind = largest_comp_id

        # print("labels - матрица, заполненная индексами компонент связности со значениями из множества: {}".format(np.unique(labels)))
        return labels == (areas[ind][0] + 1), areas[ind][2] # области нумеруются с 1, поэтому надо прибавить 1 к индексу

    def get_all_components(self) -> np.ndarray:
        return self.infos
