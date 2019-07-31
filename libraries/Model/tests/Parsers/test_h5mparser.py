#!/usr/bin/env python

import pytest
import os
from libraries.Model.Parsers.h5mparser import H5MParser as Parser
from libraries.Model.tests.globals import *


class TestH5MParser:
    def test_load_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.h5m')
        vertices = info.vertices
        indices = info.indices
        assert len(vertices) == 12
        assert len(indices) == 20

    def test_save_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.h5m')
        vertices = info.vertices
        indices = info.indices

        Parser.save_file(f'{TEST_FILES_FOLDER_PATH}/caseron_save.h5m', vertices, indices)
        info_s = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron_save.h5m')
        vertices_s = info_s.vertices
        indices_s = info_s.indices

        for v, v_s in zip(vertices, vertices_s):
            for e, e_s in zip(v, v_s):
                assert e == e_s

        for i, i_s in zip(indices, indices_s):
            for e, e_s in zip(i, i_s):
                assert e == e_s

        # Cleanup
        os.remove(f'{TEST_FILES_FOLDER_PATH}/caseron_save.h5m')

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/nonexistent.h5m')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/bad.h5m')
