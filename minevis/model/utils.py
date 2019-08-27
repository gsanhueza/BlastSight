#!/usr/bin/env python

import numpy as np
from functools import partial

from .elements.meshelement import MeshElement


def mesh_intersection(origin: np.ndarray, ray: np.ndarray, mesh: MeshElement) -> list:
    # Early detection test
    if not aabb_intersection(origin, ray, mesh):
        return []

    curry_triangle = partial(partial(triangle_intersection, origin), ray)

    triangles = mesh.vertices.view(np.ndarray)[mesh.indices]
    results = map(curry_triangle, triangles)

    return [x for x in results if x is not None]


def aabb_intersection(origin: np.ndarray, ray: np.ndarray, mesh: MeshElement):
    # Adapted from https://tavianator.com/fast-branchless-raybounding-box-intersections-part-2-nans/
    b_min, b_max = mesh.bounding_box
    b_diff = b_max - b_min

    if b_diff.min() == 0.0:  # Flat mesh means AABB unreliable
        return True

    # Result of division by zero used deliberately
    with np.errstate(divide='ignore'):
        ray_inv = 1.0 / ray

    t1 = (b_min[0] - origin[0]) * ray_inv[0]
    t2 = (b_max[0] - origin[0]) * ray_inv[0]

    tmin = min(t1, t2)
    tmax = max(t1, t2)

    for i in range(1, 3):
        t1 = (b_min[i] - origin[i]) * ray_inv[i]
        t2 = (b_max[i] - origin[i]) * ray_inv[i]

        tmin = max(tmin, min(t1, t2))
        tmax = min(tmax, max(t1, t2))

    return tmax > max(tmin, 0.0)


def triangle_intersection(origin: np.ndarray, ray: np.ndarray, triangle: np.ndarray):
    # Idea taken from https://cadxfem.org/inf/Fast%20MinimumStorage%20RayTriangle%20Intersection.pdf
    # Code adapted from https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm
    _EPSILON = 0.0000001
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


def slice_mesh(mesh: MeshElement, plane_origin: np.ndarray, plane_normal: np.ndarray) -> np.ndarray:
    # Taken from https://pypi.org/project/meshcut/
    # Although we might want to have an improved version for real-time slicing
    import meshcut
    cut = meshcut.cross_section(mesh.vertices, mesh.indices, plane_origin, plane_normal)
    return np.concatenate(cut)


def triangulate_slice(slice_vertices: np.ndarray) -> tuple:
    from .polytri import triangulate
    generator = triangulate(slice_vertices)
    gen_list = list(generator)
    triangles = np.concatenate(gen_list)
    vertices, indices = np.unique(triangles, axis=0, return_inverse=True)

    return vertices, indices


def hsv_to_rgb(hsv):
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
