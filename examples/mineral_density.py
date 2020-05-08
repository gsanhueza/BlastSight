#!/usr/bin/env python

from blastsight.view.viewer import Viewer
from blastsight.model import utils

viewer = Viewer()

mesh = viewer.load_mesh(path='../test_files/caseron.off', alpha=0.5)
blocks = viewer.load_blocks(path='../test_files/rainbow.csv')
points = viewer.load_points(path='../test_files/rainbow.csv')

vert, val, accum = utils.mineral_density(mesh=mesh.element, blocks=blocks.element, mineral='CuT')
blocks_inside = viewer.blocks(vertices=vert, values=val)

blocks.hide()

print(f'Accumulated mineral: {accum}')

viewer.fit_to_screen()
viewer.show()
