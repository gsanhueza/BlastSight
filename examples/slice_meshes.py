#!/usr/bin/env python

import numpy as np
from blastsight.view.viewer import Viewer

"""
In this demo, we'll manually slice a mesh, and detect the vertices
of that slice, so we can draw a line there.
"""

v = Viewer()

"""
First, we'll load a mesh file.
Then, we'll slice the mesh by a plane.
We need the plane's normal and any point that belongs to that plane.
"""
mesh = v.load_mesh('../test_files/caseron.off', color=[0.0, 0.0, 1.0], alpha=0.3)
origin = mesh.centroid
normal = np.array([0.2, 1.0, 0.8])

slices = v.slice_meshes(origin, normal)

"""
Then, we'll show the detected vertices.
We'll draw them as a line, so the slice is more evident.
"""

for mesh_slice in slices:
    vertices = mesh_slice.get('vertices')
    v.lines(vertices=vertices,
            color=[0.0, 1.0, 0.0],
            loop=True)

v.fit_to_screen()
v.show()
