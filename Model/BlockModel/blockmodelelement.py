#!/usr/bin/env python

from Model.modelelement import ModelElement
from Model.BlockModel.csvparser import CSVParser


# Main class
class BlockModelElement(ModelElement):
    def __init__(self):
        super().__init__()
        self.add_parser('csv', CSVParser())

        self.data: dict = None
        self.x_str: str = 'x'
        self.y_str: str = 'y'
        self.z_str: str = 'z'
        self.current_str: str = None

    def set_data(self, data: dict) -> None:
        self.data = data
        self.update_coords()

        # FIXME This should be called only when the user has already set the position strings
        self.set_value_string(self.get_available_values()[0])
        self.update_values()

    # TODO Force the user to set these strings
    def set_x_string(self, string: str) -> None:
        self.x_str = string

    def set_y_string(self, string: str) -> None:
        self.y_str = string

    def set_z_string(self, string: str) -> None:
        self.z_str = string

    def set_value_string(self, string: str) -> None:
        self.current_str = string

    def get_x_string(self) -> str:
        return self.x_str

    def get_y_string(self) -> str:
        return self.y_str

    def get_z_string(self) -> str:
        return self.z_str

    def get_value_string(self) -> str:
        return self.current_str

    def get_available_coords(self) -> list:
        return [self.x_str, self.y_str, self.z_str]

    def get_available_values(self) -> list:
        available = list(self.data.keys())
        available.remove(self.x_str)
        available.remove(self.y_str)
        available.remove(self.z_str)

        return available

    def update_coords(self):
        x = list(map(float, self.data[self.x_str]))
        y = list(map(float, self.data[self.y_str]))
        z = list(map(float, self.data[self.z_str]))

        self.set_vertices(list(zip(x, y, z)))
        self.set_indices(list(range(3 * len(self.vertices))))

    def update_values(self):
        values = list(map(float, self.data[self.current_str]))
        min_values = min(values)
        max_values = max(values)
        normalized_values = list(map(lambda val: BlockModelElement.normalize(val, min_values, max_values),
                                     values))

        self.set_values(list(map(lambda nv: [min(1.0, 2 * (1 - nv)), min(1.0, 2 * nv), 0.0], normalized_values)))

    @staticmethod
    def normalize(x: float, min_val: float, max_val: float) -> float:
        return (x - min_val)/(max_val - min_val) if max_val != min_val else 0
