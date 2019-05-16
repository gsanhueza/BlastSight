#!/usr/bin/env python

import pytest
from Model.Mesh.offparser import OFFParser


class TestOFFParser:
    def test_load_file(self):
        [vertices, indices] = OFFParser.load_file('tests/caseron.off')
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            OFFParser.load_file('nonexistent.off')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            OFFParser.load_file('tests/caseron.dxf')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            OFFParser.load_file('tests/bad.off')
