#!/usr/bin/env python

import pytest

from blastsight.model.elements.lineelement import LineElement
from blastsight.view.drawables.linegl import LineGL
from tests.view.drawables.test_gldrawable import TestGLDrawable


class TestLineGL(TestGLDrawable):
    @pytest.fixture()
    def drawable(self):
        return LineGL(LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 0.0, 0.0], id=0))

    def test_empty(self):
        with pytest.raises(Exception):
            LineGL()
