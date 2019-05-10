#!/usr/bin/env python

import pytest
from Model.parser import Parser
from Model.Mesh.offparser import OFFParser
from Model.Mesh.dxfparser import DXFParser


class TestParser:
    def generate(self):
        return Parser()


class TestDXFParser(TestParser):
    def generate(self):
        return DXFParser()


class TestOFFParser(TestParser):
    def generate(self):
        return OFFParser()
