#!/usr/bin/env python

import numpy as np

from blastsight.view.viewer import Viewer
from blastsight.model.utils import slice_mesh

v = Viewer()

meshgl = v.mesh_by_path('../test_files/blastsight.off', color=[0.0, 0.0, 1.0], alpha=0.3)
mesh = meshgl.element

slice_vertices = slice_mesh(mesh=mesh, plane_origin=mesh.centroid, plane_normal=[0.2, 1.0, 0.8])
v.lines(vertices=slice_vertices, color=[0.0, 1.0, 0.0], loop=True)

v.fit_to_screen()
v.show()
