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

            CuT = []
            idx = 0
            for elem in list_reader:
                try:
                    self.vertices.append((float(elem[0]), float(elem[1]), float(elem[2])))
                    self.indices.append(idx)
                    CuT.append(float(elem[3]))
                except ValueError:
                    continue

            min_CuT = min(CuT)
            max_CuT = max(CuT)

            for cut in CuT:
                self.values.append(
                    (min(1.0, 2 * (1.0 - self.normalize(cut, min_CuT, max_CuT))),
                     min(1.0, 2 * self.normalize(cut, min_CuT, max_CuT)),
                     0.0)
                )

    def get_indices(self) -> list:
        return self.indices  # Don't flatten

    def normalize(self, x: float, min_val: float, max_val: float) -> float:
        try:
            return (x - min_val)/(max_val - min_val)
        except ZeroDivisionError:
            return 1
