#!/usr/bin/env python

import pytest
from blastsight.model.parsers.gslibparser import GSLibParser as Parser
from tests.globals import *


class TestGSLibParser:
    def test_load(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini.out')
        data = info.get('data')
        assert data is not None
        assert data['col_0'] is not None
        assert data['col_1'] is not None
        assert data['col_2'] is not None
        assert data['col_3'] is not None

        with pytest.raises(Exception):
            assert data['abc']

    def test_load_gslib(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini_gslib.out')
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
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.out')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/blastsight.off')

    def test_save_file(self):
        with pytest.raises(Exception):
            Parser.save_file(None)
