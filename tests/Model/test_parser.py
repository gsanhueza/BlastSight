#!/usr/bin/env python

import pytest
from Model.Mesh.meshelement import MeshElement
from Model.parser import Parser
from Model.Mesh.offparser import OFFParser
from Model.Mesh.dxfparser import DXFParser


class TestParser:
    def generate(self):
        return Parser()


class TestOFFParser(TestParser):
    def generate(self):
        return OFFParser()

    def test_load_file(self):
        parser = self.generate()
        element = MeshElement()
        parser.load_file('tests/caseron.off', element)

        assert element.get_vertices().size == 3 * 12
        assert element.get_indices().size == 3 * 20


class TestDXFParser(TestParser):
    def generate(self):
        return DXFParser()

    def test_load_file(self):
        parser = self.generate()
        element = MeshElement()
        parser.load_file('tests/caseron.dxf', element)

        assert element.get_vertices().size == 3 * 12
        assert element.get_indices().size == 3 * 20
