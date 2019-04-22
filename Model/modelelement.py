#!/usr/bin/env python

import numpy as np
from PyQt5.QtCore import QFileInfo


# Main class
class ModelElement:
    def __init__(self):
        self.vertices = None
        self.indices = None
        self.values = None
        self.center = None

        self.parser_dict = {}
        self.ext = None
        self.name = None

    # FIXME Just for testing
        self.default_data()

    def default_data(self):
        self.vertices = np.array([-0.5, 0.5, 0.0,
                                  -0.5, -0.5, 0.0,
                                  0.5, 0.5, 0.0], np.float32)

        self.values = np.array([1.0, 0.0, 0.0,
                                0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0], np.float32)

        self.indices = np.array([0, 1, 2], np.uint32)  # GL_UNSIGNED_INT = np.uint32
        self.center = self.average_by_coord(self.vertices)

    def get_vertices(self):
        return self.vertices

    def get_indices(self):
        return self.indices

    def get_values(self):
        return self.values

    def set_vertices(self, vertices):
        self.vertices = np.array(vertices, np.float32)
        self.center = self.average_by_coord(self.vertices)

    def set_indices(self, indices):
        self.indices = np.array(indices, np.uint32)

    def set_values(self, values):
        self.values = np.array(values, np.float32)

    def average_by_coord(self, array):
        return np.array([array[0::3].mean(), array[1::3].mean(), array[2::3].mean()], np.float32)

    def load(self, file_path: str) -> bool:
        self.name = ModelElement.detect_file_name(file_path)
        self.ext = ModelElement.detect_file_extension(file_path)

        parser = self.get_parser(self.ext)
        parser.load_file(file_path)

        self.set_vertices(parser.get_vertices())
        self.set_indices(parser.get_indices())
        self.set_values(parser.get_values())

        return True

    def save(self, file_path: str) -> bool:
        return False

    # Adds a new parser
    def add_parser(self, extension: str, handler) -> None:
        self.parser_dict[extension] = handler

    # Returns a parser that matches the current extension
    def get_parser(self, ext: str):
        # Example: {"dxf": DXFHandler, "off": OFFHandler}
        return self.parser_dict[ext]

    @staticmethod
    def detect_file_extension(file_path: str) -> str:
        file_info = QFileInfo(file_path)
        return file_info.suffix()

    @staticmethod
    def detect_file_name(file_path: str) -> str:
        file_info = QFileInfo(file_path)
        return file_info.baseName()
