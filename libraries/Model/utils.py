#!/usr/bin/env python

import numpy as np
import operator
from functools import reduce, partial

from .Elements.meshelement import MeshElement


def mesh_intersection(origin: np.ndarray, ray: np.ndarray, mesh: MeshElement) -> bool:
    curry_triangle = partial(partial(triangle_intersection, origin), ray)

    def triangle_generator(it):
        return list(map(lambda x: mesh.vertices[it[x]], range(3)))

    triangles = map(triangle_generator, mesh.indices)
    results = map(curry_triangle, triangles)

    return reduce(operator.__or__, results)


def triangle_intersection(origin: np.ndarray, ray: np.ndarray, triangle: np.ndarray) -> bool:
    a = np.array(triangle[0])
    b = np.array(triangle[1])
    c = np.array(triangle[2])

    cross = np.cross(b - a, c - b)
    normal = cross / np.linalg.norm(cross)
    d = np.dot(cross, a)

    p = plane_intersection(origin, ray, normal, d)

    return \
        np.sign(np.dot(np.cross(b - a, p - a), normal)) == \
        np.sign(np.dot(np.cross(c - b, p - b), normal)) == \
        np.sign(np.dot(np.cross(a - c, p - c), normal))


# Taken from https://courses.cs.washington.edu/courses/cse457/09au/lectures/triangle_intersection.pdf
def plane_intersection(ray_origin: np.ndarray, ray_direction: np.ndarray,
                       plane_normal: np.ndarray, plane_d: np.ndarray) -> np.ndarray:
    t = (plane_d - np.dot(plane_normal, ray_origin)) / np.dot(plane_normal, ray_direction)

    return ray_origin + t * ray_direction
