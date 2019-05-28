#!/usr/bin/env python

import pandas as pd


class CSVParser:
    @staticmethod
    def load_file(file_path: str) -> dict:
        assert file_path.lower().endswith('csv')
        return pd.read_csv(file_path)
