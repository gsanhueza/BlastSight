#!/usr/bin/env python

from libraries.Model.Parsers.parserdata import ParserData


class TestParserData:
    def test_basic(self):
        data = ParserData()
        assert type(data.data) is dict
        assert type(data.vertices) is list
        assert type(data.indices) is list
        assert type(data.properties) is dict

    def test_empty(self):
        data = ParserData()
        assert data.data == {}
        assert data.vertices == []
        assert data.indices == []
        assert data.properties == {}

    def test_set_information(self):
        data = ParserData()
        data.data = {'a': 1, 'b': 2}
        data.vertices = [1, 2, 3]
        data.indices = [4, 5, 6, 7]
        data.properties = {'color': 'red'}

        assert 'a' in data.data.keys()
        assert 'b' in data.data.keys()
        assert 1 in data.data.values()
        assert 2 in data.data.values()

        assert len(data.vertices) == 3
        assert len(data.indices) == 4

        assert 'color' in data.properties.keys()
        assert 'red' in data.properties.values()
