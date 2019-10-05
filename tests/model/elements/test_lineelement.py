#!/usr/bin/env python

import numpy as np
import pytest
from blastsight.model.elements.lineelement import LineElement


class TestLineElement:
    def test_empty_line(self):
        with pytest.raises(Exception):
            LineElement()

    def test_single_line(self):
        element = LineElement(x=[-1, 1], y=[0, 0], z=[0, 0], color=[0.0, 1.0, 0.0])

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

    def test_multiple_lines(self):
        element = LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 1.0, 0.0])

        assert len(element.vertices) == 3

        for v in element.vertices:
            assert type(v) == np.ndarray

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

        # Color
        expected = [1.0, 1.0, 0.0]
        for i in range(len(expected)):
            assert element.color[i] == expected[i]

    def test_loop_lines(self):
        element = LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 1.0, 0.0], loop=True)
        assert len(element.vertices) == 4

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],
                    [-1.0, 0.0, 0.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_wrong_lines(self):
        with pytest.raises(Exception):
            LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0], color=[0.0, 1.0, 0.0])

        with pytest.raises(Exception):
            LineElement(x=[-1, 1, 0], y=[0, 1], z=[0, 0, 0], color=[[0.0, 1.0, 0.0]])

        with pytest.raises(Exception):
            LineElement(x=[-1], y=[0], z=[0], color=[0.0, 1.0, 0.2])

        with pytest.raises(Exception):
            LineElement(x=[-1, 1], y=[0, 1, 0], z=[0, 0, 0], values=[0.0, 1.0, 0.0])
