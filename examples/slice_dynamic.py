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

mesh = v.mesh_by_path(mesh_path,
                      color=[0.0, 0.8, 0.6],
                      alpha=0.2)
blocks = v.blocks_by_path(blocks_path)
points = v.points_by_path(blocks_path)

original_size = blocks.block_size
shrunk_size = original_size / 2

blocks.block_size = shrunk_size


"""
These two methods are taken and adapted from the application.

We offer the signals instead of automatically adding the slices,
so you can decide what to do with them before committing them
to the viewer.
"""

def slice_elements(description: dict):
    origin = description.get('origin')
    normal = description.get('normal')

    v.slice_meshes(origin, normal)
    v.slice_blocks(origin, normal)

    v.update_all()


def slot_mesh_sliced(slice_dict: dict):
    slice_list = slice_dict.get('slices', [])

    for sliced_meshes in slice_list:
        slices = sliced_meshes.get('vertices')
        origin_id = sliced_meshes.get('origin_id')
        mesh = v.get_drawable(origin_id)

        for i, vert_slice in enumerate(slices):
            v.lines(vertices=vert_slice,
                    color=mesh.color,
                    name=f'MESHSLICE_{i}_{mesh.name}',
                    extension=mesh.extension,
                    loop=True)


def slot_blocks_sliced(slice_dict: dict):
    slice_list = slice_dict.get('slices', [])

    for sliced_blocks in slice_list:
        indices = sliced_blocks.get('indices')
        origin_id = sliced_blocks.get('origin_id')
        block = v.get_drawable(origin_id)
        block.block_size = original_size

        v.blocks(vertices=block.vertices[indices],
                 values=block.values[indices],
                 color=block.color[indices],
                 vmin=block.vmin,
                 vmax=block.vmax,
                 colormap=block.colormap,
                 name=f'BLOCKSLICE_{block.name}',
                 extension=block.extension,
                 block_size=original_size,
                 alpha=1.0,
                 )

        block.block_size = shrunk_size

"""
Slice mode means that you'll click two points in the screen,
so BlastSight will automatically generate a plane that
will pass through every visible mesh and block.
"""
v.set_slice_mode()
v.signal_slice_description.connect(slice_elements)
v.signal_mesh_sliced.connect(slot_mesh_sliced)
v.signal_blocks_sliced.connect(slot_blocks_sliced)

v.fit_to_screen()
v.show()

