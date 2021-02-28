#!/usr/bin/env python

import pytest

from blastsight.view.drawables.axisgl import AxisGL
from blastsight.model.elements.nullelement import NullElement
from tests.view.drawables.test_gldrawable import TestGLDrawable


class TestAxisGL(TestGLDrawable):
    @pytest.fixture()
    def drawable(self):
        return AxisGL(NullElement(id=0))
