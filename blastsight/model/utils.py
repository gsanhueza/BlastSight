#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from colour import Color


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


def aabb_intersection(origin: np.ndarray,
                      ray: np.ndarray,
                      b_min: np.ndarray,
                      b_max: np.ndarray) -> bool:
    # Adapted from https://tavianator.com/fast-branchless-raybounding-box-intersections-part-2-nans/
    if (b_max - b_min).min() < 1e-12:  # Flat mesh means AABB unreliable
        return True

    # Result of division by zero used deliberately
    with np.errstate(divide='ignore'):
        ray_inv = 1.0 / ray

    tmin = -np.inf
    tmax = +np.inf

    for i in range(3):
        t1 = (b_min[i] - origin[i]) * ray_inv[i]
        t2 = (b_max[i] - origin[i]) * ray_inv[i]

        tmin = max(tmin, min(t1, t2))
        tmax = min(tmax, max(t1, t2))

    return tmax > max(tmin, 0.0)


def plane_intersection(origin: np.ndarray,
                       ray: np.ndarray,
                       plane_normal: np.ndarray,
                       plane_d: np.ndarray) -> np.ndarray:
    # Taken from https://courses.cs.washington.edu/courses/cse457/09au/lectures/triangle_intersection.pdf
    t = (plane_d - np.dot(plane_normal, origin)) / np.dot(plane_normal, ray)

    return origin + t * ray


def points_inside_mesh(mesh, point_vertices: np.ndarray) -> np.ndarray:
    # With ray tracing, we'll detect which points are inside the mesh
    ray = np.array([0.0, 0.0, 1.0])  # Arbitrary direction
    mask = []

    # From the point center, if we hit the mesh an odd number of times, we're inside the mesh
    for origin in point_vertices:
        intersections = mesh.intersect_with_ray(origin, ray)
        mask.append(len(intersections) > 0 and len(np.unique(intersections, axis=0)) % 2 == 1)

    return np.array(mask)


def mineral_density(mesh, blocks, mineral: str) -> tuple:
    """
    Receives a MeshElement, a BlockElement, a mineral string,
    and returns a tuple consisting of:
    (blocks inside the mesh, values of those blocks, sum of those values)

    :param mesh: MeshElement
    :param blocks: BlockElement
    :param mineral: str
    :return: tuple(np.ndarray, np.ndarray, float)
    """
    # Limit points by new bounding box of mesh and get their values
    min_bound, max_bound = mesh.bounding_box
    block_size = blocks.block_size
    half_block = block_size / 2

    # Recreate bounds to allow a block to be partially inside a mesh
    min_bound -= block_size
    max_bound += block_size

    mask = np.all((blocks.vertices > min_bound) & (blocks.vertices < max_bound), axis=-1)
    bound_blocks = blocks.vertices[mask]
    bound_values = blocks.data.get(mineral)[mask]

    # Get points inside mesh
    mask = points_inside_mesh(mesh, bound_blocks)
    insiders = np.ones(mask.size)

    # We have to check the 8 vertices to know we're not omitting a block just because its
    # center is not inside the mesh.
    # Maybe there's a better way, but we still need to investigate that.
    bias_list = [[-1, -1, -1],
                 [+1, -1, -1],
                 [-1, +1, -1],
                 [+1, +1, -1],
                 [-1, -1, +1],
                 [+1, -1, +1],
                 [-1, +1, +1],
                 [+1, +1, +1]]

    for bias in bias_list:
        mask = mask | points_inside_mesh(mesh, bound_blocks + half_block * bias)
        insiders = mask & points_inside_mesh(mesh, bound_blocks + half_block * bias)

    # TODO Calculate mineral density of blocks partially inside the mesh
    # Until now, we can only detect which blocks are fully/partially/not inside the mesh
    mask_partials = insiders ^ mask  # ^ = XOR
    # mask = mask_partials

    return bound_blocks[mask], bound_values[mask], bound_values[mask].sum()


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
