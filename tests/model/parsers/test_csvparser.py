#!/usr/bin/env python

import pytest
from minevis.model.parsers.csvparser import CSVParser as Parser
from tests.globals import *


class TestCSVParser:
    def test_load_simple_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        data = info.data
        assert data is not None
        assert data['x'] is not None
        assert data['y'] is not None
        assert data['z'] is not None
        assert data['CuT'] is not None

        with pytest.raises(Exception):
            assert data['abc']

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.off')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.csv')

    def test_load_complex_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/complex.csv')
        data = info.data
        assert data is not None
        assert data['x'] is not None
        assert data['y'] is not None
        assert data['z'] is not None
        assert data['ID'] is not None
        assert data['Cu'] is not None
        assert data['CuS'] is not None
        assert data['Cut'] is not None
        assert data['Mo'] is not None
        assert data['Au'] is not None
        assert data['Geol1'] is not None
        assert data['Geol2'] is not None
        assert data['Cat'] is not None

        with pytest.raises(Exception):
            assert data['abc']
