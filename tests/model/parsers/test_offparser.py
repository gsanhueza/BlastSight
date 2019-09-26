#!/usr/bin/env python

import pytest
from caseron.model.parsers.offparser import OFFParser as Parser
from tests.globals import *


class TestOFFParser:
    def test_load_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        vertices = info.vertices
        indices = info.indices
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.off')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.off')
