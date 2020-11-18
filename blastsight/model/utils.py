#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from colour import Color


def magnitude(vector: np.ndarray) -> float:
    return np.linalg.norm(vector)


def normalize(vector: np.ndarray) -> np.ndarray:
    return vector / magnitude(vector)


def dot_by_row(vectors_a: np.ndarray, vectors_b: np.ndarray) -> np.ndarray:
    # Returns the row-wise dot product of the input
    # Ex.: dot_by_row([v1, v2, v3], [v4, v5, v6]) = [dot(v1, v4), dot(v2, v5), dot(v3, v6)]
    return np.einsum('ij,ij->i', vectors_a, vectors_b)


def magnitude2_by_row(vectors: np.ndarray) -> np.ndarray:
    # Returns the squared magnitudes of each vector in the input
    # Ex.: magnitude2([v1, v2]) = [length(v1)^2, length(v)^2],
    # where length is the magnitude of a single vector
    return dot_by_row(vectors, vectors)


def magnitude_by_row(vectors: np.ndarray) -> np.ndarray:
    # Returns the magnitudes of each vector in the input
    # Ex.: magnitude([v1, v2]) = [length(v1), length(v2)]
    return np.sqrt(magnitude2_by_row(vectors))


def closest_point_to(origin: np.ndarray, points: np.ndarray) -> np.ndarray or None:
    if points.size == 0:
        return None

    distances = distances_between(origin, points)
    mask = np.abs(distances - distances.min()) <= 1e-12

    return points[mask][0]


def distances_between(origin: np.ndarray, points: np.ndarray) -> np.ndarray or None:
    if points.size == 0:
        return None

    return np.linalg.norm(origin - points, axis=1)


def points_inside_mesh(mesh, point_vertices: np.ndarray) -> np.ndarray:
    # With ray tracing, we'll detect which points are inside the mesh
    ray = np.array([0.0, 0.0, 1.0])  # Arbitrary direction
    mask = []

    # From the point center, if we hit the mesh an odd number of times, we're inside the mesh
    for origin in point_vertices:
        intersections = mesh.intersect_with_ray(origin, ray)
        mask.append(len(intersections) > 0 and len(np.unique(intersections, axis=0)) % 2 == 1)

    return np.array(mask)


def values_to_rgb(values: np.ndarray, vmin: float, vmax: float, colormap: str) -> np.ndarray:
    initial, final = parse_colormap(colormap)
    vals = np.interp(np.clip(values, vmin, vmax), (vmin, vmax), (0.0, 1.0))

    hsv = np.ones((vals.size, 3))
    hsv[:, 0] = initial[0] + (final - initial)[0] * vals
    hsv[:, 1] = initial[1] + (final - initial)[1] * vals
    hsv[:, 2] = initial[2] + (final - initial)[2] * vals

    return hsv_to_rgb(hsv)


def parse_colormap(colormap: str) -> list:
    try:
        initial_str, final_str = colormap.split('-')
        initial = np.array(hsl_to_hsv(*Color(initial_str).get_hsl()))
        final = np.array(hsl_to_hsv(*Color(final_str).get_hsl()))
        return [initial, final]
    except Exception:
        return []


def hsl_to_hsv(h: float, s: float, l: float) -> tuple:
    # Taken and adapted from https://gist.github.com/mathebox/e0805f72e7db3269ec22
    v = (2 * l + s * (1 - abs(2 * l - 1))) / 2
    s = 2 * (v - l) / max(v, 1e-12)
    return h, s, v


def hsv_to_rgb(hsv: np.ndarray or list) -> np.ndarray:
    # Taken and adapted from matplotlib.colors
    hsv = np.asarray(hsv)

    h = hsv[:, 0]
    s = hsv[:, 1]
    v = hsv[:, 2]

    r = np.empty_like(h)
    g = np.empty_like(h)
    b = np.empty_like(h)

    i = (h * 6.0).astype(int)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    idx = i % 6 == 0
    r[idx] = v[idx]
    g[idx] = t[idx]
    b[idx] = p[idx]

    idx = i == 1
    r[idx] = q[idx]
    g[idx] = v[idx]
    b[idx] = p[idx]

    idx = i == 2
    r[idx] = p[idx]
    g[idx] = v[idx]
    b[idx] = t[idx]

    idx = i == 3
    r[idx] = p[idx]
    g[idx] = q[idx]
    b[idx] = v[idx]

    idx = i == 4
    r[idx] = t[idx]
    g[idx] = p[idx]
    b[idx] = v[idx]

    idx = i == 5
    r[idx] = v[idx]
    g[idx] = p[idx]
    b[idx] = q[idx]

    idx = s == 0
    r[idx] = v[idx]
    g[idx] = v[idx]
    b[idx] = v[idx]

    rgb = np.stack([r, g, b], axis=-1)

    return rgb
