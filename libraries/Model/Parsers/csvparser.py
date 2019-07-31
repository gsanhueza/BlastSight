#!/usr/bin/env python

import pandas as pd
from .parserdata import ParserData


class CSVParser:
    @staticmethod
    def load_file(file_path: str) -> ParserData:
        assert file_path.lower().endswith('csv')

        with open(file_path, 'r') as f:
            data = ParserData()
            data.data = pd.read_csv(f)

            return data
