#!/usr/bin/env python

import pytest

from blastsight.model.elements.blockelement import BlockElement
from blastsight.view.drawables.blockgl import BlockGL
from tests.view.drawables.test_gldrawable import TestGLDrawable


class TestBlockGL(TestGLDrawable):
    @pytest.fixture()
    def drawable(self):
        return BlockGL(BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2], id=0))

    def test_empty(self):
        with pytest.raises(Exception):
            BlockGL()
