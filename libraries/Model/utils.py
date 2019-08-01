#!/usr/bin/env python

import numpy as np
import operator
from functools import reduce, partial

from .Elements.meshelement import MeshElement


def mesh_intersection(origin: np.ndarray, ray: np.ndarray, mesh: MeshElement) -> bool:
    curry_triangle = partial(partial(triangle_intersection, origin), ray)

    triangles = mesh.vertices.view(np.ndarray)[mesh.indices]
    results = map(curry_triangle, triangles)

    return reduce(operator.__or__, results)


def triangle_intersection(origin: np.ndarray, ray: np.ndarray, triangle: np.ndarray) -> bool:
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
        return False  # This ray is parallel to this triangle.

    f = 1.0 / a
    s = origin - vertex0
    u = f * np.dot(s, h)

    if u < 0.0 or u > 1.0:
        return False

    q = np.cross(s, edge1)
    v = f * np.dot(ray, q)

    if v < 0.0 or u + v > 1.0:
        return False

    # At this stage we can compute t to find out where the intersection point is on the line.
    t = f * np.dot(edge2, q)

    if t > _EPSILON:  # ray intersection
        intersection_point = origin + ray * t  # Here is the intersection point
        return True
    else:  # This means that there is a line intersection but not a ray intersection.
        return False
