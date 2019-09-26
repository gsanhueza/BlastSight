#!/usr/bin/env python

import numpy as np
from .element import Element


class TubeElement(Element):
    def __init__(self, *args, **kwargs):
        """
        TubeElement is a class inheriting from Element.

        {
            'data': {
                'x': list[float],
                'y': list[float],
                'z': list[float],
            }
            'properties': {
                'color': list[float],
                'alpha': float,
                'radius': float,
                'resolution': int
            },
            'metadata': {
                'id': int,
                'name': str or None,
                'extension': str or None
            }
        }
        """
        super().__init__(*args, **kwargs)

    def _fill_element(self, *args, **kwargs):
        super()._fill_element(*args, **kwargs)
        if len(self.vertices) < 2:
            raise ValueError("Not enough data to create this element.")

        if kwargs.get('loop', False):
            self.x = np.append(self.x, self.x[0])
            self.y = np.append(self.y, self.y[0])
            self.z = np.append(self.z, self.z[0])

    def _fill_properties(self, *args, **kwargs):
        super()._fill_properties(*args, **kwargs)
        self.radius = kwargs.get('radius', 0.15)
        self.resolution = kwargs.get('resolution', 15)

    """
    Properties
    """
    @property
    def radius(self) -> float:
        return self.properties.get('radius')

    @property
    def resolution(self) -> int:
        return self.properties.get('resolution')

    @radius.setter
    def radius(self, _radius: float) -> None:
        self.properties['radius'] = _radius

    @resolution.setter
    def resolution(self, _resolution: int) -> None:
        self.properties['resolution'] = _resolution

    """
    Utilities
    """
    def as_mesh(self):
        vertices = []
        indices = []
        delta = 0

        for v0, v1 in zip(self.vertices[:-1], self.vertices[1:]):
            c_vertices, c_faces = self.cylinder(self.radius, self.resolution, [v0, v1])
            vertices.append(c_vertices)
            indices.append(c_faces + delta)
            delta += (c_faces.max() + 1)

        return np.concatenate(vertices), np.concatenate(indices)

    @staticmethod
    def cylinder(radius, resolution, segment):
        # cylinder, quat_from_data and to_matrix taken and adapted from PyMesh
        Z = np.array([0.0, 0.0, 1.0])
        p0, p1 = segment

        axis = p1 - p0
        length = np.linalg.norm(axis)

        if length <= 1e-12:
            axis = Z

        angles = np.linspace(0, 2 * np.pi, resolution + 1)[:-1]
        rim = np.column_stack((np.sin(angles), np.cos(angles), np.zeros(angles.size)))
        rot = TubeElement.to_matrix(TubeElement.quat_from_data(Z, axis))

        bottom_rim = np.dot(rot, rim.T).T * radius + p0
        top_rim = np.dot(rot, rim.T).T * radius + p1

        vertices = np.vstack([[p0, p1], bottom_rim, top_rim])

        vec_resolution = np.arange(resolution)

        # Bottom fan
        bottom_fan = np.zeros((resolution, 3))
        bottom_fan[:, 0] = np.zeros(resolution)
        bottom_fan[:, 1] = np.remainder(vec_resolution + 1, resolution) + 2
        bottom_fan[:, 2] = vec_resolution + 2

        # Top fan
        top_fan = np.zeros((resolution, 3))
        top_fan[:, 0] = np.ones(resolution)
        top_fan[:, 1] = vec_resolution + resolution + 2
        top_fan[:, 2] = np.remainder(vec_resolution + 1, resolution) + resolution + 2

        # Sides
        side_a = np.zeros((resolution, 3))
        side_a[:, 0] = vec_resolution + 2
        side_a[:, 1] = np.remainder(vec_resolution + 1, resolution) + 2
        side_a[:, 2] = vec_resolution + 2 + resolution

        side_b = np.zeros((resolution, 3))
        side_b[:, 0] = vec_resolution + 2 + resolution
        side_b[:, 1] = np.remainder(vec_resolution + 1, resolution) + 2
        side_b[:, 2] = np.remainder(vec_resolution + 1, resolution) + 2 + resolution

        side = np.append(side_a, side_b).astype(np.int)
        side = side.reshape((-1, 3), order='C')

        indices = np.vstack([bottom_fan, top_fan, side])

        return vertices, indices

    @staticmethod
    def quat_from_data(v1, v2):
        eps = 1e-12
        v1 /= np.linalg.norm(v1)
        v2 /= np.linalg.norm(v2)
        c = np.dot(v1, v2)
        if c < -1.0 + eps:
            # v1 is parallel and opposite of v2
            u, s, v = np.linalg.svd(np.array([v1, v2]))
            axis = v[2, :]
        else:
            axis = np.cross(v1, v2)
            l = np.linalg.norm(axis)
            if l > 0.0:
                axis /= np.linalg.norm(axis)
            else:
                # Parallel vectors.
                axis = v1

        w_sq = 0.5 * (1.0 + c)
        l = np.sqrt(1.0 - w_sq) * axis
        quat = np.array([np.sqrt(w_sq), l[0], l[1], l[2]])

        return quat

    @staticmethod
    def to_matrix(a):
        return np.array([
            [1 - 2 * a[2] * a[2] - 2 * a[3] * a[3], 2 * a[1] * a[2] - 2 * a[3] * a[0],
             2 * a[1] * a[3] + 2 * a[2] * a[0]],
            [2 * a[1] * a[2] + 2 * a[3] * a[0], 1 - 2 * a[1] * a[1] - 2 * a[3] * a[3],
             2 * a[2] * a[3] - 2 * a[1] * a[0]],
            [2 * a[1] * a[3] - 2 * a[2] * a[0], 2 * a[2] * a[3] + 2 * a[1] * a[0],
             1 - 2 * a[1] * a[1] - 2 * a[2] * a[2]],
        ])
