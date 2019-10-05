#!/usr/bin/env python

from blastsight.view.viewer import Viewer
from blastsight.model import utils

"""
In this demo, we'll manually detect which blocks can be sliced by a plane.
"""

v = Viewer()
path = '../test_files/rainbow.csv'

"""
First, we'll load a block file.
Then, we'll slice the blocks by a plane.
We need the plane's normal and any point that belongs to that plane.
"""
blocks = v.blocks_by_path(path).element
s_blocks, s_values = utils.slice_blocks(blocks=blocks,
                                        plane_origin=blocks.center,
                                        plane_normal=[0.5, 1.0, 1.0])

"""
Finally, we'll show the detected blocks.
We'll shrink the original blocks so the difference will be more evident.
"""
blocks.block_size /= 2
v.blocks(vertices=s_blocks, values=s_values, vmin=blocks.vmin, vmax=blocks.vmax)

v.fit_to_screen()
v.show()
