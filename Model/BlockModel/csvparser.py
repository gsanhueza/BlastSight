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

            x = []
            y = []
            z = []
            CuT = []

            for elem in list_reader:
                try:
                    x.append(float(elem[0]))
                    y.append(float(elem[1]))
                    z.append(float(elem[2]))
                    CuT.append(float(elem[3]))
                except ValueError:
                    continue

            for i in range(x.__len__()):
                self.generate_cube(x[i], y[i], z[i], CuT[i], CuT, i)

    def get_indices(self) -> list:
        return self.indices

    def normalize(self, x: float, m: float, M: float) -> float:
        try:
            return (x - m)/(M - m)
        except ZeroDivisionError:
            return 1

    def generate_cube(self, x, y, z, value, value_list, index):
        # 8 vertices
        self.vertices.append((x - 1, y - 1, z - 1))
        self.vertices.append((x + 1, y - 1, z - 1))
        self.vertices.append((x - 1, y + 1, z - 1))
        self.vertices.append((x + 1, y + 1, z - 1))

        self.vertices.append((x - 1, y - 1, z + 1))
        self.vertices.append((x + 1, y - 1, z + 1))
        self.vertices.append((x - 1, y + 1, z + 1))
        self.vertices.append((x + 1, y + 1, z + 1))

        # 12 triangles
        # Front
        self.indices.append((self._vertex_pos(index, 0), self._vertex_pos(index, 1), self._vertex_pos(index, 2)))
        self.indices.append((self._vertex_pos(index, 1), self._vertex_pos(index, 3), self._vertex_pos(index, 2)))

        # Back
        self.indices.append((self._vertex_pos(index, 4), self._vertex_pos(index, 5), self._vertex_pos(index, 6)))
        self.indices.append((self._vertex_pos(index, 5), self._vertex_pos(index, 7), self._vertex_pos(index, 6)))

        # Left
        self.indices.append((self._vertex_pos(index, 0), self._vertex_pos(index, 2), self._vertex_pos(index, 6)))
        self.indices.append((self._vertex_pos(index, 0), self._vertex_pos(index, 4), self._vertex_pos(index, 6)))
        # Right
        self.indices.append((self._vertex_pos(index, 1), self._vertex_pos(index, 3), self._vertex_pos(index, 7)))
        self.indices.append((self._vertex_pos(index, 1), self._vertex_pos(index, 5), self._vertex_pos(index, 7)))

        # Top
        self.indices.append((self._vertex_pos(index, 2), self._vertex_pos(index, 3), self._vertex_pos(index, 7)))
        self.indices.append((self._vertex_pos(index, 2), self._vertex_pos(index, 6), self._vertex_pos(index, 7)))

        # Bottom
        self.indices.append((self._vertex_pos(index, 0), self._vertex_pos(index, 1), self._vertex_pos(index, 5)))
        self.indices.append((self._vertex_pos(index, 1), self._vertex_pos(index, 4), self._vertex_pos(index, 5)))

        # 8 values
        for i in range(8):
            self.values.append((min(1.0, 2.0 * (1.0 - self.normalize(value, min(value_list), max(value_list)))),
                                min(1.0, 2.0 * self.normalize(value, min(value_list), max(value_list))),
                                0.0))

    def _vertex_pos(self, index, num):
        return 8 * index + num
