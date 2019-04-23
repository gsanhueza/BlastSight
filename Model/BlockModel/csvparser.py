#!/usr/bin/env python

import csv
from Model.parser import Parser


class CSVParser(Parser):
    def __init__(self):
        super().__init__()
        self.vertices = []
        self.indices = []
        self.values = []

        # Data positions by column
        self.x_pos = 0
        self.y_pos = 1
        self.z_pos = 2

    # FIXME Not every CSV file comes with x in the first column...
    def load_csv_scheme(self, file_path: str) -> None:
        self.x_pos = 0
        self.y_pos = 1
        self.z_pos = 2

    def load_file(self, file_path: str) -> None:
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            list_reader = list(reader)

            CuT = []
            idx = 0
            for elem in list_reader:
                try:
                    self.vertices.append((float(elem[self.x_pos]),
                                          float(elem[self.y_pos]),
                                          float(elem[self.z_pos])))
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
                self.indices.append(idx)
                idx += 1

    def get_indices(self) -> list:
        return self.indices  # Don't flatten

    def normalize(self, x: float, min_val: float, max_val: float) -> float:
        try:
            return (x - min_val)/(max_val - min_val)
        except ZeroDivisionError:
            return 1
