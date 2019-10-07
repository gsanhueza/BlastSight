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
These two methods are taken and adapted from the application.

We offer the signals instead of automatically adding the slices,
so you can decide what to do with them before committing them
to the viewer.
"""


def slot_mesh_sliced(slice_dict: dict):
    slice_list = slice_dict.get('slices', [])

    for sliced_meshes in slice_list:
        slices = sliced_meshes.get('sliced_vertices')
        origin_id = sliced_meshes.get('origin_id')
        _mesh = v.get_drawable(origin_id)

        for i, vert_slice in enumerate(slices):
            v.lines(vertices=vert_slice,
                    color=_mesh.color,
                    loop=True)


def slot_blocks_sliced(slice_dict: dict):
    slice_list = slice_dict.get('slices', [])

    for sliced_blocks in slice_list:
        slices = sliced_blocks.get('sliced_vertices')
        values = sliced_blocks.get('sliced_values')
        origin_id = sliced_blocks.get('origin_id')
        _blocks = v.get_drawable(origin_id)

        v.blocks(vertices=slices,
                 values=values,
                 vmin=_blocks.vmin,
                 vmax=_blocks.vmax,
                 colormap=_blocks.colormap,
                 block_size=_blocks.block_size,
                 alpha=1.0,
                 )

    # Auto-close viewer
    v.close()


"""
Slice mode means that you'll click two points in the screen,
so BlastSight will automatically generate a plane that
will pass through every visible mesh and block.
"""
v.set_slice_mode()
v.signal_mesh_sliced.connect(slot_mesh_sliced)
v.signal_blocks_sliced.connect(slot_blocks_sliced)

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
