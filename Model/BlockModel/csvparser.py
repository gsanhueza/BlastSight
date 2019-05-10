#!/usr/bin/env python

import csv
from Model.parser import Parser


class CSVParser(Parser):
    def __init__(self):
        super().__init__()

    def load_file(self, file_path: str, model) -> None:
        with open(file_path, newline='') as f:
            reader = csv.DictReader(f)
            lr = list(reader)
            vals = list(zip(*map(lambda d: d.values(), lr)))
            data = dict(zip(lr[0], vals))

        model.set_data(data)
