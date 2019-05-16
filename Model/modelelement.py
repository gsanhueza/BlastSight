#!/usr/bin/env python

import random
import numpy as np
import traceback

from PyQt5.QtCore import QFileInfo
from statistics import mean


# Main class
class ModelElement:
    def __init__(self):
        self.vertices = np.array([], np.float32)
        self.indices = np.array([], np.uint32)
        self.values = np.array([], np.float32)
        self.centroid = np.array([], np.float32)

        self.parser_dict = {}
        self.ext = None
        self.name = None

    def get_vertices(self) -> np.array:
        return self.vertices

    def get_indices(self) -> np.array:
        return self.indices

    def get_values(self) -> np.array:
        return self.values

    def get_centroid(self) -> np.array:
        return self.centroid

    def set_vertices(self, vertices: list) -> None:
        self.vertices = np.array(vertices, np.float32)
        self.set_centroid(ModelElement.average_by_coord(self.vertices))

    def set_indices(self, indices: list) -> None:
        self.indices = np.array(indices, np.uint32)  # GL_UNSIGNED_INT = np.uint32

    def set_values(self, values: list) -> None:
        self.values = np.array(values, np.float32)

    def set_centroid(self, centroid: list) -> None:
        self.centroid = np.array(centroid, np.float32)

    @staticmethod
    def average_by_coord(array: np.array) -> list:
        # Given: [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]
        # Expected: [mean([x1, x2, x3]), mean([y1, y2, y3]), mean([z1, z2, z3])]
        return list(map(mean, zip(*array.tolist())))

    def load(self, file_path: str) -> bool:
        try:
            name = QFileInfo(file_path).baseName()
            ext = QFileInfo(file_path).suffix()

            parser = self.get_parser(ext)
            v, i = parser.load_file(file_path)
            self.set_vertices(v)
            self.set_indices(i)
            self.set_values(list(map(lambda x: random.random(), range(3))))

            self.name = name
            self.ext = ext

            return True
        except Exception:
            traceback.print_exc()
            return False

    def save(self, file_path: str) -> bool:
        return False

    # Adds a new parser
    def add_parser(self, extension: str, handler) -> None:
        self.parser_dict[extension] = handler

    # Returns a parser that matches the current extension
    def get_parser(self, ext: str):
        # Example: {"dxf": DXFHandler, "off": OFFHandler}
        return self.parser_dict[ext]
