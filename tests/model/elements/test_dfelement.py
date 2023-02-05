#!/usr/bin/env python

import pytest
import numpy as np
from blastsight.model.elements.dfelement import DFElement


class TestDFElement:
    def test_empty_element(self):
        with pytest.raises(Exception):
            DFElement()

    def test_one_points(self):
        element = DFElement(x=[0], y=[1], z=[2])
        assert len(element.vertices) == 1

        expected = [[0.0, 1.0, 2.0]]

        for i in range(len(expected)):
            assert type(element.vertices[i]) == np.ndarray
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_three_points(self):
        element = DFElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
        assert len(element.vertices) == 3

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0]]

        for i in range(len(expected)):
            assert type(element.vertices[i]) == np.ndarray
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_named_element(self):
        name = "NAME"
        extension = "EXT"
        element = DFElement(x=[0], y=[1], z=[2], name=name, extension=extension)
        assert element.name == name
        assert element.extension == extension

    def test_vertices_element(self):
        element = DFElement(vertices=[[0, 1, 2], [3, 4, 5]])

        expected = [[0.0, 1.0, 2.0],
                    [3.0, 4.0, 5.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_empty_data(self):
        with pytest.raises(Exception):
            DFElement(vertices=[])

        with pytest.raises(Exception):
            DFElement(data={})

    def test_colormap(self):
        element = DFElement(vertices=[[0, 1, 2], [3, 4, 5], [6, 7, 8]], values=[0, 1, 2])
        assert element.colormap == '#FF0000-#0000FF'
        assert element.color[0][0] == 1.0
        assert element.color[0][1] == 0.0
        assert element.color[0][2] == 0.0

        assert element.color[2][0] == 0.0
        assert element.color[2][1] == 0.0
        assert element.color[2][2] == 1.0

        element.colormap = '#00FF00-#FF0000'
        assert element.colormap == '#00FF00-#FF0000'
        assert element.color[0][0] == 0.0
        assert element.color[0][1] == 1.0
        assert element.color[0][2] == 0.0

        assert element.color[2][0] == 1.0
        assert element.color[2][1] == 0.0
        assert element.color[2][2] == 0.0

    def test_wrong_colormap(self):
        element = DFElement(vertices=[[0, 1, 2], [3, 4, 5], [6, 7, 8]], values=[0, 1, 2])
        assert element.colormap == '#FF0000-#0000FF'

        element.colormap = '#FF0000-#00FF00'
        assert element.colormap == '#FF0000-#00FF00'

        element.colormap = '#GG0000-#FFGGHH'
        assert element.colormap == '#FF0000-#00FF00'

        element.colormap = '#AA0000-#BB0000'
        assert element.colormap == '#AA0000-#BB0000'

        element.colormap = 'blah'
        assert element.colormap == '#AA0000-#BB0000'

        element.colormap = 123
        assert element.colormap == '#AA0000-#BB0000'

        element.colormap = '12-34'
        assert element.colormap == '#AA0000-#BB0000'

    def test_vmin_vmax(self):
        element = DFElement(vertices=[[0, 1, 2], [3, 4, 5], [6, 7, 8]], values=[0, 1, 2], vmin=0, vmax=1)
        assert element.vmin == 0
        assert element.vmax == 1

        assert element.colormap == '#FF0000-#0000FF'
        assert element.color[0][0] == 1.0
        assert element.color[0][1] == 0.0
        assert element.color[0][2] == 0.0

        assert element.color[1][0] == 0.0
        assert element.color[1][1] == 0.0
        assert element.color[1][2] == 1.0

        assert element.color[2][0] == 0.0
        assert element.color[2][1] == 0.0
        assert element.color[2][2] == 1.0

    def test_autocalculate_vmin_vmax(self):
        element = DFElement(vertices=[[0, 1, 2], [3, 4, 5], [6, 7, 8]], values=[0, 1, 2], vmin=0.5, vmax=1.2)
        assert element.vmin == 0.5
        assert element.vmax == 1.2

        element.recalculate_limits()

        assert element.vmin == 0.0
        assert element.vmax == 2.0

    def test_setters(self):
        element = DFElement(vertices=[[0, 1, 2]])
        element.name = 'name123'
        element.extension = 'off'
        element.alpha = 0.8

        assert element.name == 'name123'
        assert element.extension == 'off'
        assert element.alpha == 0.8

    def test_manual_color(self):
        element = DFElement(vertices=[[0, 1, 2]], color=[[1.0, 0.0, 0.0]])

        assert element.color[0][0] == 1.0
        assert element.color[0][1] == 0.0
        assert element.color[0][2] == 0.0
        assert element.alpha == 1.0

    def test_autocolor(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'val': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]}

        element = DFElement(data=data, vmin=4.0, vmax=8.0, colormap='#FF0000-#0000FF')

        expected = [
                    [1.0, 0.0, 0.0],  # Red if val < min
                    [1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],  # Green if vmin < val < vmax
                    [0.0, 0.0, 1.0],  # Blue if val > max
                    [0.0, 0.0, 1.0],
                    ]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.color[i][j] == expected[i][j]

    def test_headers(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'val1': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'val2': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]}
        element = DFElement(data=data)

        # All headers
        for header in data.keys():
            assert header in element.all_headers

        # Expected headers
        for header in data.keys():
            if header == 'val2':
                assert header not in element.headers
            else:
                assert header in element.headers

    def test_getattr_setattr(self):
        element = DFElement(vertices=[[0, 1, 2]])
        assert element.alpha == 1.0
        assert getattr(element, 'alpha') == 1.0

        setattr(element, 'alpha', 0.8)
        assert element.alpha == 0.8
        assert getattr(element, 'alpha') == 0.8

        with pytest.raises(Exception):
            setattr(element, 'wrong', 0.0)

        with pytest.raises(Exception):
            getattr(element, 'wrong')
