#!/usr/bin/env python

import numpy as np
from Model.modelelement import ModelElement
from Model.Mesh.dxfparser import DXFParser
from Model.Mesh.offparser import OFFParser


# Main class
class MeshElement(ModelElement):
    def __init__(self):
        super().__init__()
        self.add_parser('dxf', DXFParser())
        self.add_parser('off', OFFParser())

        self.normals = None

    def load(self, file_path: str):
        if super().load(file_path):
            # self.calculate_normals()

            return True
        return False

    def calculate_normals(self):
        zip_vertex_indices = list(zip(self.indices[0::3],
                                      self.indices[1::3],
                                      self.indices[2::3]))

        normals = []

        for i in range(zip_vertex_indices.__len__()):
            t = zip_vertex_indices[i]
            p1 = np.array([self.vertices[3 * t[0]], self.vertices[3 * t[0] + 1], self.vertices[3 * t[0] + 2]])
            p2 = np.array([self.vertices[3 * t[1]], self.vertices[3 * t[1] + 1], self.vertices[3 * t[1] + 2]])
            p3 = np.array([self.vertices[3 * t[2]], self.vertices[3 * t[2] + 1], self.vertices[3 * t[2] + 2]])

            print(p1, p2, p3)

            N = np.cross(p2 - p1, p3 - p1)

            normals.append(N / N.sum())

        print(normals)
        self.normals = np.array(normals, np.float32)
        print(self.normals)
