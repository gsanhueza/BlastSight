#!/usr/bin/env python

import random
from Model.modelelement import ModelElement
from Model.parser import Parser


class OFFParser(Parser):
    def __init__(self):
        super().__init__()

    def load_file(self, file_path: str, model: ModelElement) -> None:
        with open(file_path, 'r') as fp:
            assert 'OFF' == fp.readline().strip()

            n_vertices, n_faces, n_edges = tuple([int(s) for s in fp.readline().strip().split(' ')])

            # Model data
            model.set_vertices(
                Parser.flatten_tuple(
                    [[float(s) for s in fp.readline().strip().split(' ')] for _ in range(n_vertices)]
                )
            )
            model.set_indices(
                Parser.flatten_tuple(
                    [[int(s) for s in fp.readline().strip().split(' ')][1:] for _ in range(n_faces)]
                )
            )

            model.set_values(
                Parser.flatten_tuple(
                    [random.random() for _ in range(3)]
                )
            )
