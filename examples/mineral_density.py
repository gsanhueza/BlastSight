#!/usr/bin/env python

import pathlib

from blastsight.view.viewer import Viewer
from blastsight.model import utils

"""
This example is NOT READY.
At least, we can know whether a block is inside a mesh or not.
"""

viewer = Viewer()

mesh_path = f'{pathlib.Path(__file__).parent.parent}/test_files/caseron.off'
block_path = f'{pathlib.Path(__file__).parent.parent}/test_files/rainbow.csv'

mesh = viewer.load_mesh(mesh_path, alpha=0.5)
blocks = viewer.load_blocks(block_path)
points = viewer.load_points(block_path)

vert, val, accum = utils.mineral_density(mesh=mesh.element, blocks=blocks.element, mineral='CuT')
blocks_inside = viewer.blocks(vertices=vert, values=val)

blocks.hide()

print(f'Accumulated mineral: {accum}')

viewer.fit_to_screen()
viewer.show()
