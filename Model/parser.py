#!/usr/bin/env python


class Parser:
    def __init__(self):
        self.vertices = None
        self.indices = None
        self.values = None

    def load_file(self, file_path: str) -> None:
        pass

    def get_vertices(self) -> list:
        vertices = []
        indices = []

        counter = 0
        for t in self.indices:
            for i in range(t.__len__()):
                vertices += self.vertices[t[i]]
                indices.append(3 * counter + i)
            counter += 1

        return Parser.flatten_tuple(vertices)

    def get_indices(self) -> list:
        vertices = []
        indices = []

        counter = 0
        for t in self.indices:
            for i in range(t.__len__()):
                vertices += self.vertices[t[i]]
                indices.append(3 * counter + i)
            counter += 1

        return Parser.flatten_tuple(indices)

    def get_values(self) -> list:
        return Parser.flatten_tuple(self.values)

    # Flatten list of tuples
    @staticmethod
    def flatten_tuple(l: list) -> list:
        try:
            return [item for sublist in l for item in sublist]
        except TypeError:
            return l
