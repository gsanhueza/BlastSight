#!/usr/bin/env python

import pytest
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement
from Model.parser import Parser
from Model.Mesh.offparser import OFFParser
from Model.Mesh.dxfparser import DXFParser
from Model.BlockModel.csvparser import CSVParser


@pytest.fixture(autouse=True)
def parser():
    return Parser()


@pytest.fixture(autouse=True)
def offparser():
    return OFFParser()


@pytest.fixture(autouse=True)
def dxfparser():
    return DXFParser()


@pytest.fixture(autouse=True)
def csvparser():
    return CSVParser()


@pytest.fixture(autouse=True)
def meshelement():
    return MeshElement()


@pytest.fixture(autouse=True)
def bmelement():
    return BlockModelElement()


class TestParser:
    def test_init(self, parser):
        assert parser is not None


class TestOFFParser(TestParser):
    def test_load_file(self, offparser, meshelement):
        offparser.load_file('tests/caseron.off', meshelement)

        assert len(list(meshelement.get_vertices().tolist())) == 12
        assert len(list(meshelement.get_indices().tolist())) == 20


class TestDXFParser(TestParser):
    def test_load_file(self, dxfparser, meshelement):
        dxfparser.load_file('tests/caseron.dxf', meshelement)

        assert len(list(meshelement.get_vertices().tolist())) == 12
        assert len(list(meshelement.get_indices().tolist())) == 20


class TestCSVParser(TestParser):
    def test_load_file(self, csvparser, bmelement):
        csvparser.load_file('tests/mini.csv', bmelement)

        assert len(list(bmelement.get_vertices().tolist())) == 6
        assert len(list(bmelement.get_indices().tolist())) == 18
