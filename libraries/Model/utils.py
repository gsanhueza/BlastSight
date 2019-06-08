#!/usr/bin/env python

import numpy as np
import operator
from multiprocess import Pool
from functools import reduce, partial


def mesh_intersection(origin, ray, mesh) -> bool:

    curry_triangle = partial(partial(triangle_intersection, origin), ray)

    with Pool() as pool:
        triangles = pool.map(lambda it: list(map(lambda x: mesh.vertices[it[x]], range(3))), mesh.indices)
        results = pool.map(curry_triangle, triangles)

    return reduce(operator.__or__, results)


def triangle_intersection(origin, ray, triangle) -> bool:
    def sign(num):
        if num > 0:
            return 1
        elif num < 0:
            return -1
        else:
            return 0

    a = np.array(triangle[0])
    b = np.array(triangle[1])
    c = np.array(triangle[2])

    cross = np.cross(b - a, c - b)
    normal = cross / np.linalg.norm(cross)
    d = np.dot(cross, a)

    p = plane_intersection(origin, ray, normal, d)

    return \
        sign(np.dot(np.cross(b - a, p - a), normal)) == \
        sign(np.dot(np.cross(c - b, p - b), normal)) == \
        sign(np.dot(np.cross(a - c, p - c), normal))


# Taken from https://courses.cs.washington.edu/courses/cse457/09au/lectures/triangle_intersection.pdf
def plane_intersection(ray_origin, ray_direction, plane_normal, plane_d) -> np.ndarray:
    t = (plane_d - np.dot(plane_normal, ray_origin)) / np.dot(plane_normal, ray_direction)

    return ray_origin + t * ray_direction
