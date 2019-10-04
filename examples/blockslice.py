#!/usr/bin/env python

import time

from caseron.view.viewer import Viewer
from caseron.model import utils

v = Viewer()
path = '../test_files/rainbow.csv'

start = time.time()
block_element = v.model.blocks_by_path(path)
print(f'Loading time: {time.time() - start} seconds.')

start = time.time()
s_blocks, s_values = utils.slice_blocks(blocks=block_element,
                                        plane_origin=block_element.center,
                                        plane_normal=[0.5, 1.0, 1.0])

print(f'Slicing time: {time.time() - start} seconds.')

v.points_by_path(path)
v.blocks(vertices=s_blocks, values=s_values, vmin=block_element.vmin, vmax=block_element.vmax)

v.fit_to_screen()
v.show()
