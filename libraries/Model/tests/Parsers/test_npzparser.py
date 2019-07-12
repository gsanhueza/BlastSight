#!/usr/bin/env python

import pytest
from libraries.Model.Parsers.npzparser import NPZParser as Parser
from libraries.Model.tests.globals import *


class TestNPZParser:
    def test_load_file(self):
        [vertices, indices] = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.npz')
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.npz')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.npz')
