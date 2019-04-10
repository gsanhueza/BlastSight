#!/usr/bin/env python

from PySide2.QtCore import QFileInfo


class Handler:
    def __init__(self):
        self.parser_dict = {}

    # Adds a new handler for meshes
    def add_parser(self, extension: str, handler) -> None:
        self.parser_dict[extension] = handler

    # Returns the handler that matches the current extension
    def get_parser(self, ext: str):
        # Example: {"dxf": DXFHandler, "off": OFFHandler}
        return self.parser_dict[ext]

    def load(self, model, file_path: str) -> bool:
        return False

    def save(self, model, file_path: str) -> bool:
        return False

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        file_info = QFileInfo(file_path)
        return file_info.suffix()
