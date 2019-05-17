#!/usr/bin/env python

import pytest
from Model.Parsers.offparser import OFFParser

TEST_FILES_FOLDER_PATH = 'tests/files'


class TestOFFParser:
    def test_load_file(self):
        [vertices, indices] = OFFParser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            OFFParser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.off')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            OFFParser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            OFFParser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.off')
