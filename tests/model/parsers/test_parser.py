#!/usr/bin/env python

import pytest
from caseron.model.parsers.parser import Parser
from tests.globals import *


class TestParser:
    def test_load(self):
        with pytest.raises(NotImplementedError):
            Parser.load_file(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

    def test_save(self):
        with pytest.raises(NotImplementedError):
            Parser.save_file(f'{TEST_FILES_FOLDER_PATH}/mini.csv', {})
