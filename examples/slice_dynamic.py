#!/usr/bin/env python

import pathlib

from blastsight.view.viewer import Viewer

"""
In this demo, a mesh and a block set will be dynamically sliced by yourself,
by clicking in two parts of the screen.
"""

viewer = Viewer()
title = viewer.windowTitle()
viewer.setWindowTitle(f'{title} - Click two points in the screen.')

mesh_path = f'{pathlib.Path(__file__).parent.parent}/test_files/caseron.off'
block_path = f'{pathlib.Path(__file__).parent.parent}/test_files/rainbow.csv'

mesh = viewer.load_mesh(mesh_path, color=[0.0, 0.8, 0.6], alpha=0.2)
blocks = viewer.load_blocks(block_path, alpha=0.1)

original_size = blocks.block_size


def slice_elements(description: dict) -> None:
    """
    The method slice_elements reacts to viewer.signal_slice_description,
    and receives a description of the slice, so you can do whatever you
    want with that information.

    :param description: Description of the cross-section
    :return: None
    """
    origin = description.get('origin')
    normal = description.get('normal')

    # Retrieve slices
    mesh_slices = viewer.slice_meshes(origin, normal)
    block_slices = viewer.slice_blocks(origin, normal)

    # Add slices to the viewer
    add_mesh_slices(mesh_slices)
    add_blocks_slices(block_slices)

    # Update the viewer
    viewer.update_all()


def add_mesh_slices(slice_list: list) -> None:
    for sliced_meshes in slice_list:
        slices = sliced_meshes.get('vertices')
        origin_id = sliced_meshes.get('element_id')
        mesh = viewer.get_drawable(origin_id)

        for i, vert_slice in enumerate(slices):
            viewer.lines(vertices=vert_slice,
                         color=mesh.color,
                         name=f'MESHSLICE_{i}_{mesh.name}',
                         extension=mesh.extension,
                         loop=True)


def add_blocks_slices(slice_list: list) -> None:
    for sliced_blocks in slice_list:
        indices = sliced_blocks.get('indices')
        origin_id = sliced_blocks.get('element_id')
        block = viewer.get_drawable(origin_id)

        viewer.blocks(vertices=block.vertices[indices],
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


"""
Slice mode means that you'll click two points in the screen,
so BlastSight will automatically generate a plane that
will pass through every visible mesh and block.
"""
viewer.set_slice_controller()
viewer.signal_slice_description.connect(slice_elements)

viewer.fit_to_screen()
viewer.show()
