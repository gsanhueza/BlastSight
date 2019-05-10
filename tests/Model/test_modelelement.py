#!/usr/bin/env python

import pytest
import numpy as np
from Model.modelelement import ModelElement
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


class TestModelElement:
    def test_init(self):
        element = ModelElement()
        assert element is not None

        element = MeshElement()
        assert element is not None

        element = BlockModelElement()
        assert element is not None

    def test_empty_mesh(self):
        element = MeshElement()
        assert type(element.get_vertices()) is np.ndarray
        assert type(element.get_indices()) is np.ndarray
        assert type(element.get_values()) is np.ndarray
        assert type(element.get_centroid()) is np.ndarray

    def test_set_mesh_vertices(self):
        element = MeshElement()
        data = [[0.0, 1.0, 2.0]]
        element.set_vertices(data)

        element_data = element.get_vertices()

        for i in range(len(data)):
            assert all(element_data[i]) == all(data[i])

    def test_set_mesh_indices(self):
        element = MeshElement()
        data = [0, 1, 2]
        element.set_indices(data)

        element_data = element.get_indices()

        for i in range(len(data)):
            assert element_data[i] == data[i]

    def test_set_mesh_values(self):
        element = MeshElement()
        data = [0.0, 1.0, 2.0]
        element.set_values(data)

        element_data = element.get_values()

        for i in range(len(data)):
            assert element_data[i] == data[i]
