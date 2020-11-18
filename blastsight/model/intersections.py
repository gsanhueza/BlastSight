#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
from . import utils


class Intersections:
    @staticmethod
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

    @staticmethod
    def ray_with_plane(origin: np.ndarray,
                       ray: np.ndarray,
                       plane_normal: np.ndarray,
                       plane_d: float) -> np.ndarray:
        # Taken from https://courses.cs.washington.edu/courses/cse457/09au/lectures/triangle_intersection.pdf
        t = (plane_d - np.dot(plane_normal, origin)) / np.dot(plane_normal, ray)

        return origin + t * ray

    @staticmethod
    def ray_with_triangles(origin: np.ndarray,
                           ray: np.ndarray,
                           triangles: np.ndarray) -> np.ndarray:
        # Idea taken from https://cadxfem.org/inf/Fast%20MinimumStorage%20RayTriangle%20Intersection.pdf
        # Code adapted from https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm
        # Manually vectorized to benefit from numpy's performance.

        # Get individual vertices of each triangle
        triangles = triangles.flatten().reshape((-1, 3))
        vertex0 = triangles[0::3]
        vertex1 = triangles[1::3]
        vertex2 = triangles[2::3]

        edge1 = vertex1 - vertex0
        edge2 = vertex2 - vertex0

        # Note: Both np.inner(a, b).diagonal() and np.dot(a, b.T)
        # run out of memory, but (a * b).sum(axis=1) does not,
        # so we're using that one instead.
        h = np.cross(ray, edge2)
        a = (edge1 * h).sum(axis=1)

        mask = abs(a) > 1e-12  # False => Ray is parallel to triangle.

        # Result of division by zero used deliberately
        with np.errstate(divide='ignore', invalid='ignore'):
            f = 1.0 / a  # Can this be solved in a more elegant way?
            s = origin - vertex0
            u = f * (s * h).sum(axis=1)

            mask = (0.0 <= u) & (u <= 1.0) & mask

            q = np.cross(s, edge1)
            v = f * (ray * q).sum(axis=1)

            mask = (v >= 0.0) & (u + v <= 1.0) & mask

            # At this stage we can compute t to find out where the intersection point is on the line.
            t = f * (edge2 * q).sum(axis=1)

            mask = (t > 1e-12) & mask  # Ray intersections

        # Here are the intersections.
        return np.unique(origin + ray * t[mask].reshape(-1, 1), axis=0)

    @staticmethod
    def ray_with_lines(origin: np.ndarray,
                       ray: np.ndarray,
                       vertices: np.ndarray,
                       threshold: float = 1e-2) -> np.ndarray:
        # Adapted from https://www.codefull.net/2015/06/intersection-of-a-ray-and-a-line-segment-in-3d/

        ba = np.diff(vertices, axis=0)
        ao = vertices[:-1] - origin

        ao_x_ba = np.cross(ao, ba)
        ray_x_ba = np.cross(ray, ba)

        # How much does the ray need to travel to arrive to the (infinite) line, for each segment
        s = utils.dot_by_row(ao_x_ba, ray_x_ba) / utils.magnitude2_by_row(ray_x_ba)

        # All intersections with infinite lines
        intersections = origin + s.reshape(-1, 1) * ray

        length_ai = utils.magnitude_by_row(intersections - vertices[:-1])
        length_ib = utils.magnitude_by_row(intersections - vertices[1:])
        length_ab = utils.magnitude_by_row(ba)

        # Mask is True if the ray and line are coplanar enough
        mask_threshold = abs(utils.dot_by_row(ao, ray_x_ba)) < threshold

        # Mask is True if the ray is between the start and end of each segment
        mask_inside = length_ai + length_ib <= length_ab + threshold

        return intersections[mask_threshold & mask_inside]
