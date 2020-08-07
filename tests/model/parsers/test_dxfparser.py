#!/usr/bin/env python

import pytest
from blastsight.model.parsers.dxfparser import DXFParser as Parser
from tests.globals import *


class TestDXFParser:
    def test_load_mesh(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf', hint='mesh')
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_load_lines(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/polyline3d.dxf', hint='line')
        vertices = info.get('data').get('vertices')
        assert len(vertices) == 9

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.dxf')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.off')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.dxf')

    def test_save_file(self):
        with pytest.raises(Exception):
            Parser.save_file(None)
