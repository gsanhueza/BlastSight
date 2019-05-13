#!/usr/bin/env python

import numpy as np
from Model.modelelement import ModelElement
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


class TestModelElement:
    def generate(self):
        return ModelElement()

    def test_empty_mesh(self):
        element = self.generate()
        assert type(element.get_vertices()) is np.ndarray
        assert type(element.get_indices()) is np.ndarray
        assert type(element.get_values()) is np.ndarray
        assert type(element.get_centroid()) is np.ndarray

    def test_set_vertices(self):
        element = self.generate()
        data = [[0.0, 1.0, 2.0]]
        element.set_vertices(data)

        element_data = element.get_vertices()

        for i in range(len(data)):
            assert all(element_data[i]) == all(data[i])

    def test_set_indices(self):
        element = self.generate()
        data = [0, 1, 2]
        element.set_indices(data)

        element_data = element.get_indices()

        for i in range(len(data)):
            assert element_data[i] == data[i]

    def test_set_values(self):
        element = self.generate()
        data = [0.0, 1.0, 2.0]
        element.set_values(data)

        element_data = element.get_values()

        for i in range(len(data)):
            assert element_data[i] == data[i]


class TestMeshElement(TestModelElement):
    def generate(self):
        return MeshElement()


class TestBlockModelElement(TestModelElement):
    def generate(self):
        return BlockModelElement()
