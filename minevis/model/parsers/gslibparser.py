#!/usr/bin/env python

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class GSLibParser(Parser):
    @staticmethod
    def load_file(path: str) -> ParserData:
        assert path.lower().endswith('out')

        # Metadata
        properties = {
            'name': QFileInfo(path).completeBaseName(),
            'ext': QFileInfo(path).suffix()
        }

        header_count, headers = GSLibParser.get_header_info(path)

        with open(path, 'r') as f:
            data = ParserData()
            data.data = pd.read_csv(f, sep=' ', header=None, names=headers, skiprows=header_count + 2)
            data.properties = properties

            return data

    @staticmethod
    def save_file(*args, **kwargs) -> None:
        raise NotImplementedError

    @staticmethod
    def get_header_info(path: str) -> tuple:
        with open(path, 'r') as gslib_file:
            gslib_file.readline()
            header_count = int(gslib_file.readline().strip().split()[0])
            headers = [gslib_file.readline().strip().split()[0] for _ in range(header_count)]
            return header_count, headers
