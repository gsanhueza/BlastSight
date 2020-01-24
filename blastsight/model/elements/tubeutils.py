#!/usr/bin/env python

# These methods are taken and adapted from PyMesh.
# https://github.com/PyMesh/PyMesh
#
# PyMesh's license is Mozilla Public License 2, and as such,
# this particular file must be licensed as MPL2.
#
# See https://www.mozilla.org/en-US/MPL/ for more info.

import numpy as np


def cylinder(radius: float, resolution: int, segment: tuple) -> tuple:
    Z = np.array([0.0, 0.0, 1.0])
    p0, p1 = segment

    axis = p1 - p0
    length = np.linalg.norm(axis)

    if length <= 1e-12:
        axis = Z

    angles = np.linspace(0, 2 * np.pi, resolution + 1)[:-1]
    rim = np.column_stack((np.sin(angles), np.cos(angles), np.zeros(angles.size)))
    rot = to_matrix(quat_from_data(Z, axis))

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


def quat_from_data(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
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


def to_matrix(a: np.ndarray) -> np.ndarray:
    return np.array([
        [1 - 2 * a[2] * a[2] - 2 * a[3] * a[3], 2 * a[1] * a[2] - 2 * a[3] * a[0],
         2 * a[1] * a[3] + 2 * a[2] * a[0]],
        [2 * a[1] * a[2] + 2 * a[3] * a[0], 1 - 2 * a[1] * a[1] - 2 * a[3] * a[3],
         2 * a[2] * a[3] - 2 * a[1] * a[0]],
        [2 * a[1] * a[3] - 2 * a[2] * a[0], 2 * a[2] * a[3] + 2 * a[1] * a[0],
         1 - 2 * a[1] * a[1] - 2 * a[2] * a[2]],
    ])
