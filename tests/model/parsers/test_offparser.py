#!/usr/bin/env python

import pytest
import os
from blastsight.model.parsers.offparser import OFFParser as Parser
from tests.globals import *


class TestOFFParser:
    def test_load_file(self):
        info = Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')
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

    def test_save_file(self):
        info = Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')

        properties = {'color': [1.0, 0.6, 0.2], 'alpha': 0.5}

        Parser.save_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron_save.off',
                         vertices=vertices, indices=indices, properties=properties)
        Parser.save_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron_save.off',
                         data={'vertices': vertices, 'indices': indices}, properties=properties)
        Parser.save_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron_save.off',
                         data={'x': vertices[:, 0],
                               'y': vertices[:, 1],
                               'z': vertices[:, 2],
                               'indices': indices}, properties=properties)
        info_s = Parser.load_file(path=f'{TEST_FILES_FOLDER_PATH}/caseron_save.off')
        vertices_s = info_s.get('data').get('vertices')
        indices_s = info_s.get('data').get('indices')
        metadata_s = info_s.get('metadata')

        for v, v_s in zip(vertices, vertices_s):
            for e, e_s in zip(v, v_s):
                assert abs(e - e_s) < 1e-12

        for i, i_s in zip(indices, indices_s):
            for e, e_s in zip(i, i_s):
                assert abs(e - e_s) < 1e-12

        assert metadata_s.get('name') == 'caseron_save'
        assert metadata_s.get('extension') == 'off'

        # Cleanup
        os.remove(f'{TEST_FILES_FOLDER_PATH}/caseron_save.off')

    def test_save_empty(self):
        with pytest.raises(Exception):
            Parser.save_file()
        with pytest.raises(Exception):
            Parser.save_file(None)
