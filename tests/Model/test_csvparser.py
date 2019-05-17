#!/usr/bin/env python

import pytest
from Model.Parsers.csvparser import CSVParser

TEST_FILES_FOLDER_PATH = 'tests/files'


class TestDXFParser:
    def test_load_simple_file(self):
        data = CSVParser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        assert type(data) == dict

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            CSVParser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            CSVParser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini.xls')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            CSVParser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.csv')

    def test_load_complex_file(self):
        data = CSVParser.load_file(f'{TEST_FILES_FOLDER_PATH}/complex.csv')
        assert type(data) == dict
