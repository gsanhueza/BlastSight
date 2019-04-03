#!/usr/bin/env python

from abc import abstractmethod


class Parser:
    def __init__(self):
        self.vertices = None
        self.indices = None

    @abstractmethod
    def load_file(self, file_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_vertices(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_indices(self) -> list:
        raise NotImplementedError

    # Flatten list of tuples
    def _flatten_tuple(self, l):
        return [item for sublist in l for item in sublist]
