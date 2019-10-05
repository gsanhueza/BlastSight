#!/usr/bin/env python

from blastsight.view.viewer import Viewer
from blastsight.model import utils

"""
In this demo, we'll manually slice a mesh, and detect the vertices
of that slice, so we can draw a line there.
"""

v = Viewer()

mesh = v.mesh_by_path('../test_files/caseron.off', color=[0.0, 0.0, 1.0], alpha=0.3).element

slice_vertices = utils.slice_mesh(mesh=mesh, plane_origin=mesh.centroid, plane_normal=[0.2, 1.0, 0.8])
v.lines(vertices=slice_vertices, color=[0.0, 1.0, 0.0], loop=True)

v.fit_to_screen()
v.show()
