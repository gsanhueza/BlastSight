#!/usr/bin/env python

import numpy as np
import pathlib

from blastsight.view.viewer import Viewer

"""
In this demo, we'll manually detect which blocks can be sliced by a plane.
"""

v = Viewer()
path = f'{pathlib.Path(__file__).parent.parent}/test_files/rainbow.csv'

"""
First, we'll load a block file.
Then, we'll slice the blocks by a plane.
We need the plane's normal and any point that belongs to that plane.
"""
blocks = v.load_blocks(path)
origin = blocks.center
normal = np.array([0.5, 1.0, 1.0])

slices = v.slice_blocks(origin, normal)

"""
Then, we'll show the detected blocks.
"""
for block_slice in slices:
    # The slices list has only one item because we only have one block element
    element_id = block_slice.get('element_id')
    element = v.get_drawable(element_id)  # element == blocks in this example

    indices = block_slice.get('indices')

    v.blocks(vertices=element.vertices[indices],
             values=element.values[indices],
             vmin=element.vmin,
             vmax=element.vmax,
             block_size=element.block_size)

"""
We'll shrink the original blocks so the difference will be more evident.
"""
blocks.block_size /= 2

v.fit_to_screen()
v.show()
