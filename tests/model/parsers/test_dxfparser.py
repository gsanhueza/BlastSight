#!/usr/bin/env python

import pytest
from blastsight.model.parsers.dxfparser import DXFParser as Parser
from tests.globals import *


class TestDXFParser:
    def test_load_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.dxf')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.off')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.dxf')
