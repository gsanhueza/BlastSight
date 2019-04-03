#!/usr/bin/env python

from abc import abstractmethod
from PySide2.QtCore import QFileInfo


class Handler:
    def __init__(self):
        pass

    @abstractmethod
    def load_mesh(self, model, file_path):
        return False

    @abstractmethod
    def save_mesh(self, model, file_path):
        return False

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        file_info = QFileInfo(file_path)
        return file_info.suffix()
