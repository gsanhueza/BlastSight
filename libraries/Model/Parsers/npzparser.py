#!/usr/bin/env python

import numpy as np


# https://stackoverflow.com/questions/35133317/numpy-save-some-arrays-at-once
class NPZParser:
    @staticmethod
    def load_file(file_path: str) -> tuple:
        assert file_path.lower().endswith('npz')

        with np.load(file_path) as data:
            return data['vertices'], data['indices']
