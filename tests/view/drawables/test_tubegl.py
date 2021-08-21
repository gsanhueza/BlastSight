#!/usr/bin/env python

import pytest

from blastsight.model.elements.tubeelement import TubeElement
from blastsight.view.drawables.tubegl import TubeGL
from tests.view.drawables.test_gldrawable import TestGLDrawable


class TestTubeGL(TestGLDrawable):
    @pytest.fixture()
    def drawable(self):
        return TubeGL(TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 0.0, 0.0], id=0))

    def test_empty(self):
        with pytest.raises(Exception):
            TubeGL()

    def test_single_color(self, drawable):
        drawable.initialize()
        assert len(drawable.color.reshape((-1, 3))) == 1

    def test_multiple_colors(self, drawable):
        drawable.color = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
        drawable.initialize()
        assert len(drawable.color.reshape((-1, 3))) == 3
