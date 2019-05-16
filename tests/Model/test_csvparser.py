#!/usr/bin/env python

import pytest
from Model.BlockModel.csvparser import CSVParser


class TestDXFParser:
    def test_load_simple_file(self):
        data = CSVParser.load_file('tests/mini.csv')
        assert type(data) == dict

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            CSVParser.load_file('tests/nonexistent.csv')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            CSVParser.load_file('tests/mini.xls')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            CSVParser.load_file('tests/bad.csv')

    def test_load_complex_file(self):
        data = CSVParser.load_file('tests/complex.csv')
        assert type(data) == dict
