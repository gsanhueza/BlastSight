#!/usr/bin/env python

from .meshgl import MeshGL


class BatchMeshGL(MeshGL):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element)

    def setup_attributes(self) -> None:
        pass

    def draw(self):
        pass
