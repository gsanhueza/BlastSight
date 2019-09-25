#!/usr/bin/env python

import meshcut
import numpy as np

from colour import Color
from functools import partial


def mesh_intersection(origin: np.ndarray, ray: np.ndarray, mesh) -> list:
    # Early detection test
    if not aabb_intersection(origin, ray, mesh):
        return []

    curry_triangle = partial(partial(triangle_intersection, origin), ray)

    triangles = mesh.vertices[mesh.indices]
    results = map(curry_triangle, triangles)

    return [x for x in results if x is not None]


def aabb_intersection(origin: np.ndarray, ray: np.ndarray, mesh):
    # Adapted from https://tavianator.com/fast-branchless-raybounding-box-intersections-part-2-nans/
    b_min, b_max = mesh.bounding_box
    b_diff = b_max - b_min

    if b_diff.min() < 1e-12:  # Flat mesh means AABB unreliable
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


def plane_intersection(origin: np.ndarray, ray: np.ndarray,
                       plane_normal: np.ndarray, plane_d: np.ndarray) -> np.ndarray:
    # Taken from https://courses.cs.washington.edu/courses/cse457/09au/lectures/triangle_intersection.pdf
    t = (plane_d - np.dot(plane_normal, origin)) / np.dot(plane_normal, ray)

    return origin + t * ray


def triangle_intersection(origin: np.ndarray, ray: np.ndarray, triangle: np.ndarray) -> list or None:
    # Idea taken from https://cadxfem.org/inf/Fast%20MinimumStorage%20RayTriangle%20Intersection.pdf
    # Code adapted from https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm
    _EPSILON = 1e-12
    vertex0 = triangle[0]
    vertex1 = triangle[1]
    vertex2 = triangle[2]

    edge1 = vertex1 - vertex0
    edge2 = vertex2 - vertex0

    h = np.cross(ray, edge2)
    a = np.dot(edge1, h)

    if -_EPSILON < a < _EPSILON:
        return None  # This ray is parallel to this triangle.

    f = 1.0 / a
    s = origin - vertex0
    u = f * np.dot(s, h)

    if u < 0.0 or u > 1.0:
        return None

    q = np.cross(s, edge1)
    v = f * np.dot(ray, q)

    if v < 0.0 or u + v > 1.0:
        return None

    # At this stage we can compute t to find out where the intersection point is on the line.
    t = f * np.dot(edge2, q)

    if t > _EPSILON:  # ray intersection
        intersection_point = origin + ray * t  # Here is the intersection point
        return intersection_point

    # This means that there is a line intersection but not a ray intersection.
    return None


def slice_mesh(mesh, plane_origin: np.ndarray, plane_normal: np.ndarray) -> list:
    # Taken from https://pypi.org/project/meshcut/
    # Although we might want to have an improved version.
    # This returns a list with the slices (in case we have a concave mesh)
    try:
        return meshcut.cross_section(mesh.vertices, mesh.indices, plane_origin, plane_normal)
    except AssertionError:
        # Meshcut doesn't want to slice
        print(f'WARNING: Mesh {mesh.name} (id = {mesh.id}) cannot be sliced, fix your mesh!')
        return []


def slice_blocks(blocks, plane_origin: np.ndarray, plane_normal: np.ndarray) -> list:
    """
    Plane Equation: ax + by + cz + d = 0
    Where [a, b, c] = plane_normal
    Where [x, y, z] = plane_origin (or any point that we know belongs to the plane)

    With this, we can get `d`:
    dot([a, b, c], [x, y, z]) + d = 0
    d = -dot([a, b, c], [x, y, z])

    Since we have multiple vertices, it's easier to multiply plane_normal with
    each vertex, and manually sum them to get an array of dot products.

    But our points are blocks (they have 3D dimensions in `block_size`).
    That means we have to tolerate more points, so we create a threshold.
    Plane Inequation: abs(ax + by + cz + d) < threshold

    Where threshold will be the half of largest diagonal a cube can have to
    realistically touch a plane.
    For example: sqrt(x^2 + x^2 + x^2) = x * sqrt(3.0) / 2.0

    I should get a better threshold, but this will have to suffice for now.
    """
    block_size = blocks.block_size
    vertices = blocks.vertices
    threshold = np.sqrt(np.power(block_size / 2, 2).sum())  # Half a cube's diagonal

    plane_d = -np.dot(plane_normal, plane_origin)
    mask = np.abs((plane_normal * vertices).sum(axis=1) + plane_d) < threshold

    return vertices[mask]


def hsl_to_hsv(h, s, l):
    # Taken and adapted from https://gist.github.com/mathebox/e0805f72e7db3269ec22
    v = (2 * l + s * (1 - abs(2 * l - 1))) / 2
    s = 2 * (v - l) / max(v, 1e-12)
    return h, s, v


def parse_colormap(colormap: str) -> list:
    try:
        initial_str, final_str = colormap.split('-')
        initial = np.array(hsl_to_hsv(*Color(initial_str).get_hsl()))
        final = np.array(hsl_to_hsv(*Color(final_str).get_hsl()))
        return [initial, final]
    except Exception:
        return []


def values_to_rgb(values: np.ndarray, vmin: float, vmax: float, colormap: str) -> np.ndarray:
    initial, final = parse_colormap(colormap)
    vals = np.interp(np.clip(values, vmin, vmax), (vmin, vmax), (0.0, 1.0))

    hsv = np.ones((vals.size, 3))
    hsv[:, 0] = initial[0] + (final - initial)[0] * vals
    hsv[:, 1] = initial[1] + (final - initial)[1] * vals
    hsv[:, 2] = initial[2] + (final - initial)[2] * vals

    return hsv_to_rgb(hsv)


def hsv_to_rgb(hsv: list) -> np.ndarray:
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


def mineral_density(mesh, blocks, mineral: str) -> tuple:
    min_bound, max_bound = mesh.bounding_box
    block_size = blocks.block_size

    # Set value string to match what we're looking for
    old_val = blocks.value_str
    blocks.value_str = mineral

    # Recreate bounds to allow a block to be partially inside a mesh
    min_bound = min_bound - block_size
    max_bound = max_bound + block_size

    # Limit blocks by new bounding box of mesh and get their values
    mask = np.all((blocks.vertices > min_bound) & (blocks.vertices < max_bound), axis=-1)
    B = blocks.vertices[mask]
    values = blocks.values[mask]

    # Restore original value string
    blocks.values_str = old_val

    # With ray tracing, we'll detect which blocks are truly inside the mesh
    ray = np.array([0.0, 0.0, 1.0])  # Arbitrary direction
    idx_inside = []

    # From the block, if we hit the mesh an odd number of times, we're inside the mesh
    for origin in B:
        intersections = mesh_intersection(origin, ray, mesh)
        idx_inside.append(len(intersections) > 0 and (np.unique(intersections, axis=0).size // 3) % 2 == 1)

    # TODO Detect blocks near the borders (partial value)

    return B[idx_inside], values[idx_inside], values[idx_inside].sum()
