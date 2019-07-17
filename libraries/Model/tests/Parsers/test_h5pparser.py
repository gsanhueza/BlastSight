#!/usr/bin/env python

import os
import pytest
from libraries.Model.Parsers.h5pparser import H5PParser as Parser
from libraries.Model.tests.globals import *


class TestH5PParser:
    def test_load_simple_file(self):
        data = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini.h5p')
        assert data is not None
        assert data['x'] is not None
        assert data['y'] is not None
        assert data['z'] is not None
        assert data['CuT'] is not None

        with pytest.raises(Exception):
            assert data['abc']

    def test_save_file(self):
        data = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini.h5p')
        Parser.save_file(f'{TEST_FILES_FOLDER_PATH}/mini_save.h5p', data)
        data_s = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini_save.h5p')

        for k, k_s in zip(data.keys(), data_s.keys()):
            assert k == k_s

        for v, v_s in zip(data.values, data_s.values):
            for e, e_s in zip(v, v_s):
                assert e == e_s

        # Cleanup
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_save.h5p')

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.h5p')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.off')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.h5p')

    def test_load_complex_file(self):
        data = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/complex.h5p')
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
