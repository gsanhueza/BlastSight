#!/usr/bin/env python

import numpy as np
from Model.modelelement import ModelElement
from Model.parser import Parser


class CSVParser(Parser):
    def __init__(self):
        super().__init__()

        # Data positions by column
        self.x_pos = 0
        self.y_pos = 1
        self.z_pos = 2

    # TODO Not every CSV file comes with x in the first column...
    def load_csv_scheme(self, file_path: str) -> None:
        self.x_pos = 0
        self.y_pos = 1
        self.z_pos = 2

    def load_file(self, file_path: str, model: ModelElement) -> None:
        vertices = []
        indices = []
        values = []

        CuT = []
        idx = 0
        for elem in np.loadtxt(file_path, delimiter=',', skiprows=1):
            try:
                vertices.append((float(elem[self.x_pos]),
                                 float(elem[self.y_pos]),
                                 float(elem[self.z_pos])))
                CuT.append(float(elem[3]))
            except ValueError:
                continue

        min_CuT = min(CuT)
        max_CuT = max(CuT)

        for cut in CuT:
            values.append(
                (min(1.0, 2 * (1.0 - CSVParser.normalize(cut, min_CuT, max_CuT))),
                 min(1.0, 2 * CSVParser.normalize(cut, min_CuT, max_CuT)),
                 0.0)
            )
            indices.append(idx)
            idx += 1

        # Model data
        model.set_vertices(vertices)
        model.set_indices(indices)
        model.set_values(values)

    @staticmethod
    def normalize(x: float, min_val: float, max_val: float) -> float:
        try:
            return (x - min_val)/(max_val - min_val)
        except ZeroDivisionError:
            return 1
