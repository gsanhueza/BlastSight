#!/usr/bin/env python

import numpy as np


def generate_vertices(x, y):
    k = 0
    vertices = []

    min_x = -(x - 1) // 2
    max_x = +(x + 1) // 2

    min_y = -(y - 1) // 2
    max_y = +(y + 1) // 2

    for j in range(min_y, max_y):
        for i in range(min_x, max_x):
            vertices.append([i, j, k])
    
    return np.array(vertices, np.float32)


def generate_indices(x, y):
    indices = []

    for j in range(0, x * (y - 1), x):
        for i in range(x - 1):
            t1 = [i + j, i + j + 1, i + j + x]
            t2 = [i + j + 1, i + j + x, i + j + x + 1]
            indices.append(t1)
            indices.append(t2)
            
    return np.array(indices, np.uint32)


def generate_grid(x, y):
    return generate_vertices(x, y), generate_indices(x, y)


def generate_off(vertices, indices, filename):
    num_v = vertices.size // 3
    num_i = indices.size // 3
    num_e = num_v + num_i - 2

    with open(filename, 'w') as f:
        f.write('OFF\n')
        f.write(f'{num_v} {num_i} {num_e}\n')

        # Vertices
        for v in vertices:
            vv = v.tolist()
            f.write(f'{vv[0]} {vv[1]} {vv[2]}\n')

        # Indices
        for i in indices:
            f.write(f'3 {i[0]} {i[1]} {i[2]}\n')


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        x = 15
        y = 15
    else:
        x = int(sys.argv[1])
        y = int(sys.argv[2])

    v, i = generate_grid(x, y)
    generate_off(v, i, 'grid.off')

