#!/usr/bin/env python

import csv


class CSVParser:
    @staticmethod
    def load_file(file_path: str) -> dict:
        assert file_path.lower().endswith('csv')

        with open(file_path, newline='') as f:
            reader = csv.DictReader(f)
            lr = list(reader)
            vals = list(zip(*map(lambda d: d.values(), lr)))
            data = dict(zip(lr[0], vals))

        return data
