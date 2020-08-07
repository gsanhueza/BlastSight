#!/usr/bin/env python

import pytest
import os
from blastsight.model.parsers.h5mparser import H5MParser as Parser
from tests.globals import *


class TestH5MParser:
    def test_load_file(self):
        info = Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron.h5m')
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')
        metadata = info.get('metadata')

        assert len(vertices) == 12
        assert len(indices) == 20
        assert metadata.get('name') == 'caseron'
        assert metadata.get('extension') == 'h5m'

    def test_save_file(self):
        info = Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron.h5m')
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')

        properties = {'color': [1.0, 0.6, 0.2], 'alpha': 0.5}

        Parser.save_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron_save.h5m',
                         vertices=vertices, indices=indices, properties=properties)
        info_s = Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron_save.h5m')
        vertices_s = info_s.get('data').get('vertices')
        indices_s = info_s.get('data').get('indices')
        properties_s = info_s.get('properties')
        metadata_s = info_s.get('metadata')

        for v, v_s in zip(vertices, vertices_s):
            for e, e_s in zip(v, v_s):
                assert abs(e - e_s) < 1e-12

        for i, i_s in zip(indices, indices_s):
            for e, e_s in zip(i, i_s):
                assert abs(e - e_s) < 1e-12

        assert metadata_s.get('name', '') == 'caseron_save'
        assert metadata_s.get('extension', '') == 'h5m'

        assert len(properties_s.get('color', [])) == 3
        assert properties_s.get('color', [])[0] == 1.0
        assert properties_s.get('color', [])[1] == 0.6
        assert properties_s.get('color', [])[2] == 0.2
        assert properties_s.get('alpha', 0.0) == 0.5

        # Cleanup
        os.remove(f'{TEST_FILES_FOLDER_PATH}/caseron_save.h5m')

    def test_load_inexistent(self):
        with pytest.raises(Exception):
            Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/nonexistent.h5m')

    def test_load_wrong_extension(self):
        with pytest.raises(Exception):
            Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')

    def test_load_damaged(self):
        with pytest.raises(Exception):
            Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/bad.h5m')

    def test_save_empty(self):
        with pytest.raises(Exception):
            Parser.save_file()
