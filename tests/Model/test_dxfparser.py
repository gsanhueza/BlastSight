#!/usr/bin/env python

import pytest
from Model.Mesh.dxfparser import DXFParser


class TestDXFParser:
    def test_load_file(self):
        [vertices, indices] = DXFParser.load_file('tests/caseron.dxf')
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            DXFParser.load_file('tests/nonexistent.dxf')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            DXFParser.load_file('tests/caseron.off')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            DXFParser.load_file('tests/bad.dxf')
