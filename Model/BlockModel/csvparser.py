#!/usr/bin/env python

import csv
from Model.modelelement import ModelElement
from Model.parser import Parser


class CSVParser(Parser):
    def __init__(self):
        super().__init__()

    def load_file(self, file_path: str, model: ModelElement) -> None:
        with open(file_path, newline='') as f:
            reader = csv.DictReader(f)
            lr = list(reader)
            vals = list(zip(*map(lambda d: d.values(), lr)))
            data = dict(zip(lr[0], map(list, vals)))

        # FIXME Those hardcoded strings are in the header of the CSV file
        x = [float(s) for s in data['x']]
        y = [float(s) for s in data['y']]
        z = [float(s) for s in data['z']]
        CuT = [float(s) for s in data['CuT']]
        min_CuT = min(CuT)
        max_CuT = max(CuT)

        values = []
        for cut in CuT:
            values.append(
                (min(1.0, 2 * (1.0 - CSVParser.normalize(cut, min_CuT, max_CuT))),
                 min(1.0, 2 * CSVParser.normalize(cut, min_CuT, max_CuT)),
                 0.0)
            )

        vertices = list(zip(x, y, z))
        indices = list(range(3 * len(vertices)))

        model.set_vertices(vertices)
        model.set_indices(indices)
        model.set_values(values)

    @staticmethod
    def normalize(x: float, min_val: float, max_val: float) -> float:
        return (x - min_val)/(max_val - min_val) if max_val != min_val else 0
