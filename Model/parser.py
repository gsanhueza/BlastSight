#!/usr/bin/env python


class Parser:
    def __init__(self):
        self.vertices = None
        self.indices = None
        self.values = None

    def load_file(self, file_path: str) -> None:
        pass

    def get_vertices(self) -> list:
        return Parser.flatten_tuple(self.vertices)

    def get_indices(self) -> list:
        return Parser.flatten_tuple(self.indices)

    def get_values(self) -> list:
        return Parser.flatten_tuple(self.values)

    # Flatten list of tuples
    @staticmethod
    def flatten_tuple(l: list) -> list:
        import time
        start_time = time.time()

        ans = None
        try:
            ans = [item for sublist in l for item in sublist]
        except TypeError:
            ans = l

        print(f'flatten_tuple: {time.time() - start_time}')

        return ans
