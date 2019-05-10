#!/usr/bin/env python

import pytest
from Model.parser import Parser


class TestParser:
    def test_init(self):
        parser = Parser()
        assert parser is not None
