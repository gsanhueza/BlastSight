#!/usr/bin/env python

from PySide2.QtCore import QFileInfo


# Main class
class ModelElement:
    def __init__(self):
        self.vertices = None
        self.indices = None
        self.values = None

        self.parser_dict = {}

    def get_vertices(self):
        return self.vertices

    def get_indices(self):
        return self.indices

    def get_values(self):
        return self.values

    def set_vertices(self, vertices):
        self.vertices = vertices

    def set_indices(self, indices):
        self.indices = indices

    def set_values(self, values):
        self.values = values

    def load(self, file_path: str) -> bool:
        ext = ModelElement.get_file_extension(file_path)

        parser = self.get_parser(ext)
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
    def get_file_extension(file_path: str) -> str:
        file_info = QFileInfo(file_path)
        return file_info.suffix()
