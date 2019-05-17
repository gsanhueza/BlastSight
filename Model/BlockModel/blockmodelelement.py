#!/usr/bin/env python

import colorsys
import numpy as np
from Model.element import Element


class BlockModelElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = kwargs.get('data')
        self.x_str = kwargs.get('easting')
        self.y_str = kwargs.get('northing')
        self.z_str = kwargs.get('elevation')
        self.current_str = kwargs.get('value')

        self.values = np.array([], np.float32)
        self.centroid = np.array([], np.float32)

    def _init_fill(self, *args, **kwargs):
        pass

    def set_vertices(self, vertices: list) -> None:
        self.x, self.y, self.z = zip(*vertices)
        self.set_centroid(Element.average_by_coord(self.get_vertices()))

    def set_centroid(self, centroid: list) -> None:
        self.centroid = np.array(centroid, np.float32)

    def set_values(self, values: list) -> None:
        self.values = np.array(values, np.float32)

    def set_data(self, data: dict) -> None:
        self.data = data

    def get_values(self) -> np.array:
        return self.values

    def get_centroid(self) -> np.array:
        return self.centroid

    # TODO Force the user to set these strings
    def set_x_string(self, string: str) -> None:
        self.x_str = string

    def set_y_string(self, string: str) -> None:
        self.y_str = string

    def set_z_string(self, string: str) -> None:
        self.z_str = string

    def set_value_string(self, string: str) -> None:
        self.current_str = string

    def get_x_string(self) -> str:
        return self.x_str

    def get_y_string(self) -> str:
        return self.y_str

    def get_z_string(self) -> str:
        return self.z_str

    def get_value_string(self) -> str:
        return self.current_str

    def get_available_coords(self) -> list:
        if self.x_str is None:
            return list(self.data.keys())

        return sorted([self.x_str, self.y_str, self.z_str])

    def get_available_values(self) -> list:
        available = list(self.data.keys())

        if self.x_str is not None:
            available.remove(self.x_str)
            available.remove(self.y_str)
            available.remove(self.z_str)

        return available

    def update_coords(self):
        x = list(map(float, self.data[self.x_str]))
        y = list(map(float, self.data[self.y_str]))
        z = list(map(float, self.data[self.z_str]))

        self.set_vertices(list(zip(x, y, z)))

    def update_values(self):
        values = list(map(float, self.data[self.current_str]))
        min_values = min(values)
        max_values = max(values)

        normalized_values = map(lambda val: BlockModelElement.normalize(val, min_values, max_values), values)
        self.set_values(list(map(lambda hue: colorsys.hsv_to_rgb(hue, 1.0, 1.0), normalized_values)))

    @staticmethod
    def normalize(x: float, min_val: float, max_val: float) -> float:
        return (x - min_val) / (max_val - min_val) if max_val != min_val else 0
