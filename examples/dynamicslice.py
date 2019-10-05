#!/usr/bin/env python

from blastsight.view.viewer import Viewer
from blastsight.model import utils

"""
In this demo, a mesh and a block set will be sliced by yourself.
"""

v = Viewer()
title = v.windowTitle()
v.setWindowTitle(f'{title} - Click two points in the screen.')
mesh_path = '../test_files/caseron.off'
blocks_path = '../test_files/rainbow.csv'

mesh = v.mesh_by_path(mesh_path, color=[0.0, 0.8, 0.6], alpha=0.6)
blocks = v.blocks_by_path(blocks_path)
points = v.points_by_path(blocks_path)

"""
Slice mode means that you'll click two points in the screen,
so BlastSight will automatically generate a plane that
will pass through every visible mesh and block.
"""
v.set_slice_mode()
v.signal_file_modified.connect(v.close)

v.fit_to_screen()
v.show()

"""
When you click twice, the window will close and re-open
with a more evident result of your slice.
"""
v.setWindowTitle(title)
mesh.alpha = 0.2
blocks.hide()

v.update_all()
v.show()
