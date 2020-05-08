#!/usr/bin/env python

import numpy
from blastsight.view.viewer import Viewer

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
blocks = v.load_blocks(path)
description = v.model.slice_blocks(block_list=[blocks],
                                   origin=blocks.center,
                                   plane_normal=[0.5, 1.0, 1.0])

indices = description.get('slices')[0].get('indices')

"""
Then, we'll show the detected blocks.
"""
v.blocks(vertices=blocks.vertices[indices],
         values=blocks.values[indices],
         vmin=blocks.vmin,
         vmax=blocks.vmax,
         block_size=blocks.block_size)

"""
We'll shrink the original blocks so the difference will be more evident.
"""
blocks.block_size /= 2

v.fit_to_screen()
v.show()
