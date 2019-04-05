#!/usr/bin/env python

import csv
from Model.parser import Parser


class CSVParser(Parser):
    def __init__(self):
        super().__init__()
        self.vertices = []
        self.indices = []
        self.values = []

    def load_file(self, file_path: str) -> None:
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            list_reader = list(reader)

            i = 0
            CuT = []

            for elem in list_reader:
                try:
                    self.vertices.append((float(elem[0]) - 6295, float(elem[1]) - 5950, float(elem[2]) - 2025))
                    CuT.append(float(elem[3]))
                    self.indices.append(i)
                    i += 1
                except ValueError:
                    continue

            _CuT = self.normalize(CuT, min(CuT), max(CuT))
            for c in _CuT:
                r = min(1.0, 2 * (1.0 - c))
                g = min(1.0, 2 * c)
                b = 0
                self.values.append((r, g, b))

    def get_indices(self) -> list:
        return self.indices

    def normalize(self, l: list, m: float, M: float) -> list:
        return [((x - m)/(M - m)) for x in l]
