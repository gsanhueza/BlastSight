#!/usr/bin/env python

import numpy as np
import pytest
from blastsight.model.elements.tubeelement import TubeElement


class TestTubeElement:
    def test_empty_tube(self):
        with pytest.raises(Exception):
            TubeElement()

    def test_single_tube(self):
        element = TubeElement(x=[-1, 1], y=[0, 0], z=[0, 0], color=[0.0, 1.0, 0.0])

        assert len(element.vertices) == 2

        for v in element.vertices:
            assert type(v) == np.ndarray

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

        # Color
        expected = [0.0, 1.0, 0.0]
        for i in range(len(expected)):
            assert element.color[i] == expected[i]

    def test_multiple_tubes(self):
        element = TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 1.0, 0.0])

        assert len(element.vertices) == 3

        for v in element.vertices:
            assert type(v) == np.ndarray

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

        # Color
        expected = [1.0, 1.0, 0.0]
        for i in range(len(expected)):
            assert element.color[i] == expected[i]

    def test_loop_tubes(self):
        element = TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 1.0, 0.0], loop=True)
        assert len(element.vertices) == 4

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],
                    [-1.0, 0.0, 0.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_wrong_tubes(self):
        with pytest.raises(Exception):
            TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0], color=[0.0, 1.0, 0.0])

        with pytest.raises(Exception):
            TubeElement(x=[-1, 1, 0], y=[0, 1], z=[0, 0, 0], color=[[0.0, 1.0, 0.0]])

        with pytest.raises(Exception):
            TubeElement(x=[-1], y=[0], z=[0], color=[0.0, 1.0, 0.2])

        with pytest.raises(Exception):
            TubeElement(x=[-1, 1], y=[0, 1, 0], z=[0, 0, 0], values=[[0.0, 1.0, 0.0]])

    def test_radius_resolution(self):
        element = TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 1.0, 0.0])

        assert element.radius == 0.15
        assert element.resolution == 15

        element = TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 1.0, 0.0],
                              radius=0.2, resolution=12)

        assert element.radius == 0.2
        assert element.resolution == 12

        element.radius = 0.3
        element.resolution = 9

        assert element.radius == 0.3
        assert element.resolution == 9
