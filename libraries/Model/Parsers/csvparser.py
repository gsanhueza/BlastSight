#!/usr/bin/env python

import pandas as pd


class CSVParser:
    @staticmethod
    def load_file(file_path: str) -> dict:
        assert file_path.lower().endswith('csv')

        with open(file_path, 'r') as f:
            return pd.read_csv(f)
