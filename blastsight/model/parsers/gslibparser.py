#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pandas as pd
from qtpy.QtCore import QFileInfo
from .parserdata import ParserData
from .parser import Parser


class GSLibParser(Parser):
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> ParserData:
        assert path.lower().endswith('out')

        # Metadata
        properties = {
            'name': QFileInfo(path).completeBaseName(),
            'extension': QFileInfo(path).suffix()
        }

        data = ParserData()
        try:
            header_count, headers = GSLibParser.get_header_info(path)
            with open(path, 'r') as f:
                data.data = pd.read_csv(f, sep=' ', header=None, names=headers, skiprows=header_count + 2)
                data.properties = properties
        except Exception:  # This "GSLib" file doesn't have headers
            print(f'*** WARNING: We can read {path}, but keep in mind that this not a real GSLib file. ***')
            with open(path, 'r') as f:
                data.data = pd.read_csv(f, sep=' ', header=None, prefix='col_')
                data.properties = properties

        return data

    @staticmethod
    def get_header_info(path: str) -> tuple:
        with open(path, 'r') as gslib_file:
            gslib_file.readline()
            header_count = int(gslib_file.readline().strip().split()[0])
            headers = [gslib_file.readline().strip().split()[0] for _ in range(header_count)]
            return header_count, headers
