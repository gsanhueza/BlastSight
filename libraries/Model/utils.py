#!/usr/bin/env python

import numpy as np
from functools import partial

from .Elements.meshelement import MeshElement


def mesh_intersection(origin: np.ndarray, ray: np.ndarray, mesh: MeshElement) -> list:
    # Early detection test
    if not aabb_intersection(origin, ray, mesh):
        return []

    curry_triangle = partial(partial(triangle_intersection, origin), ray)

    triangles = mesh.vertices.view(np.ndarray)[mesh.indices]
    results = map(curry_triangle, triangles)

    return [x for x in results if x is not None]


def aabb_intersection(origin, ray, mesh):
    # Adapted from https://tavianator.com/fast-branchless-raybounding-box-intersections-part-2-nans/
    b_min = np.array([mesh.x.min(), mesh.y.min(), mesh.z.min()])
    b_max = np.array([mesh.x.max(), mesh.y.max(), mesh.z.max()])
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
