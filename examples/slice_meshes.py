#!/usr/bin/env python

from blastsight.view.viewer import Viewer
from blastsight.model import utils

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
mesh = v.mesh_by_path('../test_files/caseron.off',
                      color=[0.0, 0.0, 1.0],
                      alpha=0.3).element

description = v.model.slice_meshes(meshes=[mesh],
                                   origin=mesh.centroid,
                                   plane_normal=[0.2, 1.0, 0.8])

slices = description.get('slices')

"""
Then, we'll show the detected vertices.
We'll draw them as a line, so the slice is more evident.
"""

for m_slice in slices:
    vertices = m_slice.get('vertices')
    v.lines(vertices=vertices,
            color=[0.0, 1.0, 0.0],
            loop=True)

v.fit_to_screen()
v.show()
