#!/usr/bin/env python

import pytest

from blastsight.model.elements.tubeelement import TubeElement
from blastsight.view.drawables.tubelegacygl import TubeLegacyGL
from tests.view.drawables.test_tubegl import TestTubeGL


class TestTubLegacyGL(TestTubeGL):
    @pytest.fixture()
    def drawable(self):
        return TubeLegacyGL(TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 0.0, 0.0], id=0))

    def test_empty(self):
        with pytest.raises(Exception):
            TubeLegacyGL()
