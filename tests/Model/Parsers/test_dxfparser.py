#!/usr/bin/env python

import pytest
from Model.Parsers.dxfparser import DXFParser

from tests.globals import *


class TestDXFParser:
    def test_load_file(self):
        [vertices, indices] = DXFParser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            DXFParser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.dxf')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            DXFParser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.off')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            DXFParser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.dxf')
