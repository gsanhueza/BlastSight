#!/usr/bin/env python

import numpy as np
import traceback

from PyQt5.QtCore import QFileInfo
from statistics import mean


# Main class
class ModelElement:
    def __init__(self):
        self.vertices = np.ndarray([], np.float32)
        self.indices = np.ndarray([], np.uint32)
        self.values = np.ndarray([], np.float32)
        self.centroid = np.ndarray([], np.float32)

        self.parser_dict = {}
        self.ext = None
        self.name = None

    def get_vertices(self) -> np.ndarray:
        return self.vertices

    def get_indices(self) -> np.ndarray:
        return self.indices

    def get_values(self) -> np.ndarray:
        return self.values

    def get_centroid(self) -> np.ndarray:
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
    def average_by_coord(array: np.ndarray) -> list:
        # Given: [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]
        # Expected: [mean([x1, x2, x3]), mean([y1, y2, y3]), mean([z1, z2, z3])]
        return list(map(mean, zip(*array.tolist())))

    def load(self, file_path: str) -> bool:
        try:
            name = QFileInfo(file_path).baseName()
            ext = QFileInfo(file_path).suffix()

            parser = self.get_parser(ext)
            parser.load_file(file_path, self)

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
