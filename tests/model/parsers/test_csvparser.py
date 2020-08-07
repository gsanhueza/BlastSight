#!/usr/bin/env python

import os
import pytest
from blastsight.model.parsers.csvparser import CSVParser as Parser
from tests.globals import *


class TestCSVParser:
    def test_load_simple_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        data = info.get('data')
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
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/blastsight.off')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.csv')

    def test_load_complex_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/complex.csv')
        data = info.get('data')
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

    def test_save_file(self):
        info = Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        data = info.get('data')
        Parser.save_file(path=f'{TEST_FILES_FOLDER_PATH}/mini_save.csv', data=data)

        info_s = Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/mini_save.csv')
        data_s = info_s.get('data')

        for k, k_s in zip(data.keys(), data_s.keys()):
            assert k == k_s

        for v, v_s in zip(data.values, data_s.values):
            for e, e_s in zip(v, v_s):
                assert e == e_s

        # Cleanup
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_save.csv')

    def test_save_empty(self):
        with pytest.raises(Exception):
            Parser.save_file()
