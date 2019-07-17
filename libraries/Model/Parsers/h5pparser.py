#!/usr/bin/env python

import pandas as pd


class H5PParser:
    @staticmethod
    def load_file(file_path: str):
        assert file_path.lower().endswith('.h5p')
        return pd.read_hdf(file_path, 'data')

    @staticmethod
    def save_file(file_path: str, data) -> None:
        path = file_path if file_path.endswith('.h5p') else f'{file_path}.h5p'
        data.to_hdf(path, 'data')
