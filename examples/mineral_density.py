#!/usr/bin/env python

from blastsight.view.viewer import Viewer
from blastsight.model.utils import mineral_density

viewer = Viewer()

mesh = viewer.mesh_by_path(path='../test_files/caseron.off', alpha=0.5)
blocks = viewer.blocks_by_path(path='../test_files/rainbow.csv')
points = viewer.points_by_path(path='../test_files/rainbow.csv')

vert, val, accum = mineral_density(mesh=mesh.element, blocks=blocks.element, mineral='CuT')
blocks_inside = viewer.blocks(vertices=vert, values=val)

blocks.hide()

print(f'Mineral accum: {accum}')

viewer.fit_to_screen()
viewer.show()
