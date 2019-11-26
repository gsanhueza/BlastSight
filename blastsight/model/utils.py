#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import meshcut
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


def mesh_intersection(origin: np.ndarray, ray: np.ndarray, mesh) -> np.ndarray:
    # Early AABB detection test
    if not aabb_intersection(origin, ray, *mesh.bounding_box):
        return np.empty(0)

    return vectorized_triangles_intersection(origin, ray, mesh.vertices[mesh.indices])


def aabb_intersection(origin: np.ndarray, ray: np.ndarray, b_min: np.ndarray, b_max: np.ndarray) -> bool:
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


def plane_intersection(origin: np.ndarray, ray: np.ndarray,
                       plane_normal: np.ndarray, plane_d: np.ndarray) -> np.ndarray:
    # Taken from https://courses.cs.washington.edu/courses/cse457/09au/lectures/triangle_intersection.pdf
    t = (plane_d - np.dot(plane_normal, origin)) / np.dot(plane_normal, ray)

    return origin + t * ray


def triangle_intersection(origin: np.ndarray, ray: np.ndarray, triangle: np.ndarray) -> np.ndarray or None:
    try:
        intersection = vectorized_triangles_intersection(origin, ray, triangle)
    except IndexError:
        intersection = vectorized_triangles_intersection(origin, ray, np.array([triangle]))

    return intersection[0] if intersection.size > 0 else None


def vectorized_triangles_intersection(origin: np.ndarray,
                                      ray: np.ndarray,
                                      triangles: np.ndarray) -> np.ndarray:
    # Idea taken from https://cadxfem.org/inf/Fast%20MinimumStorage%20RayTriangle%20Intersection.pdf
    # Code adapted from https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm
    # Manually vectorized to benefit from numpy's performance.

    # Get individual vertices of each triangle
    vertex0 = triangles[:, 0, :]
    vertex1 = triangles[:, 1, :]
    vertex2 = triangles[:, 2, :]

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
    return origin + ray * t[mask].reshape(-1, 1)  # Here are the intersections.


def slice_mesh(mesh,
               plane_origin: np.ndarray or list,
               plane_normal: np.ndarray or list) -> list:
    # Taken from https://pypi.org/project/meshcut/
    # Although we might want to have an improved version.
    # This returns a list with the slices (in case we have a concave mesh)
    try:
        return meshcut.cross_section(mesh.vertices, mesh.indices, np.array(plane_origin), np.array(plane_normal))
    except AssertionError:
        # Meshcut doesn't want to slice
        print(f'WARNING: Mesh {mesh.name} (id = {mesh.id}) cannot be sliced, fix your mesh!')
        return []


def slice_blocks(blocks,
                 block_size: np.ndarray or list,
                 plane_origin: np.ndarray or list,
                 plane_normal: np.ndarray or list) -> np.ndarray:
    """
    *** Plane Equation: ax + by + cz + d = 0 ***

    Where [a, b, c] = plane_normal
    Where [x, y, z] = plane_origin (or any point that we know belongs to the plane)

    With this, we can get `d`:
    dot([a, b, c], [x, y, z]) + d = 0
    d = -dot([a, b, c], [x, y, z])

    Since we have multiple vertices, it's easier to multiply plane_normal with
    each vertex, and manually sum them to get an array of dot products.

    But our points are blocks (they have 3D dimensions in `block_size`).
    That means we have to tolerate more points, so we create a threshold.

    *** Plane Inequation: abs(ax + by + cz + d) <= threshold ***

    We need to know how inclined is the plane normal to know our threshold.
    Let's say our block_size is [10, 10, 10] (half_block is [5, 5, 5]).

    If the plane touches one face of the cube, our threshold is [-5, +5] * np.sqrt(1.0).
    If the plane touches one edge of the cube, our threshold is [-5, +5] * np.sqrt(2.0).
    If the plane touches one vertex of the cube, our threshold is [-5, +5] * np.sqrt(3.0).

    Since a cube is symmetrical by axes, we don't really care about the plane normal's signs.
    Then, we'll calculate np.dot(abs(plane_normal), half_block) to know the maximum
    tolerable distance between the cube center and its projection on the plane.

    The projection idea comes from
    https://gdbooks.gitbooks.io/3dcollisions/content/Chapter2/static_aabb_plane.html
    """
    plane_normal /= np.linalg.norm(plane_normal)
    half_block = np.array(block_size) / 2
    vertices = blocks.vertices

    plane_d = -np.dot(plane_normal, plane_origin)
    threshold = np.dot(np.abs(plane_normal), half_block)

    # In this context, np.inner(a, b) returns the same as (a * b).sum(axis=1), but it's faster.
    # Luckily, we don't run out of memory like in vectorized_triangles_intersection.
    mask = np.abs(np.inner(plane_normal, vertices) + plane_d) <= threshold

    return mask_to_indices(mask)


def slice_points(points,
                 point_size: float,
                 plane_origin: np.ndarray or list,
                 plane_normal: np.ndarray or list) -> np.ndarray:

    return slice_blocks(points, 3 * [point_size], plane_origin, plane_normal)


def points_inside_mesh(mesh, point_vertices: np.ndarray) -> np.ndarray:
    # With ray tracing, we'll detect which points are inside the mesh
    ray = np.array([0.0, 0.0, 1.0])  # Arbitrary direction
    mask = []

    # From the point center, if we hit the mesh an odd number of times, we're inside the mesh
    for origin in point_vertices:
        intersections = mesh_intersection(origin, ray, mesh)
        mask.append(len(intersections) > 0 and (np.unique(intersections, axis=0).size // 3) % 2 == 1)

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


def mask_to_indices(mask: np.ndarray) -> np.ndarray:
    # If mask = [True, False, True], then mask.nonzero()[-1] = [0, 2]
    return mask.nonzero()[-1]


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

