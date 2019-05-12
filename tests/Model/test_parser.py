#!/usr/bin/env python

import pytest
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement
from Model.parser import Parser
from Model.Mesh.offparser import OFFParser
from Model.Mesh.dxfparser import DXFParser
from Model.BlockModel.csvparser import CSVParser


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

        assert len(list(element.get_vertices().tolist())) == 12
        assert len(list(element.get_indices().tolist())) == 20


class TestDXFParser(TestParser):
    def generate(self):
        return DXFParser()

    def test_load_file(self):
        parser = self.generate()
        element = MeshElement()
        parser.load_file('tests/caseron.dxf', element)

        assert len(list(element.get_vertices().tolist())) == 12
        assert len(list(element.get_indices().tolist())) == 20


class TestCSVParser(TestParser):
    def generate(self):
        return CSVParser()

    def test_load_file(self):
        parser = self.generate()
        element = BlockModelElement()
        parser.load_file('tests/mini.csv', element)

        assert len(list(element.get_vertices().tolist())) == 6
        assert len(list(element.get_indices().tolist())) == 18
