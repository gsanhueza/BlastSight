#!/usr/bin/env python

from abc import abstractmethod


class Parser:
    def __init__(self):
        self.vertices = None
        self.faces = None

    @abstractmethod
    def load_file(self, filepath: str) -> None:
        pass
