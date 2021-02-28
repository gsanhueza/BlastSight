#!/usr/bin/env python

import pytest

from blastsight.view.drawables.backgroundgl import BackgroundGL
from blastsight.model.elements.nullelement import NullElement
from tests.view.drawables.test_gldrawable import TestGLDrawable


class TestBackgroundGL(TestGLDrawable):
    @pytest.fixture()
    def drawable(self):
        return BackgroundGL(NullElement(id=0))

    @staticmethod
    def equal_list(la, lb) -> bool:
        return all(map(lambda x, y: x == y, la, lb))

    def test_colors(self, drawable):
        top = [0.1, 0.2, 0.3]
        bot = [0.4, 0.5, 0.6]

        assert self.equal_list(top, drawable.top_color)
        assert self.equal_list(bot, drawable.bottom_color)

        top = [0.2, 0.4, 0.6]
        bot = [0.6, 0.4, 0.2]

        drawable.top_color = top
        drawable.bottom_color = bot

        assert self.equal_list(top, drawable.top_color)
        assert self.equal_list(bot, drawable.bottom_color)
