#!/usr/bin/env python

import numpy as np
import pathlib

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show how you can animate a cross-section so you can simulate that you're scanning a mine.

A Cross-Section is equivalent as slicing a mesh, but without returning the vertices of each slice.
This means that we can easily generate a cross-section of all the rendered meshes in real time.

Internally, it's a visual effect, which means we have to manually activate the cross-section mode
with 'v.set_cross_section(True). This activates the cross-section with default values for the plane.

You can change the plane description with v.cross_section(origin, normal), where 'origin' is a point
on the plane, and 'normal' is the normal of the plane.

To deactivate the cross-section, just use 'v.set_cross_section(False)'.

"""

v = Viewer()
mesh_path = f'{pathlib.Path(__file__).parent.parent}/test_files/caseron.off'
block_path = f'{pathlib.Path(__file__).parent.parent}/test_files/rainbow.csv'

mesh = v.load_mesh(mesh_path, color=[1.0, 0.8, 0.0])
blocks = v.load_blocks(block_path)
low, high = v.bounding_box()


def scan(origin):
    v.cross_section(origin, np.array([1.0, 0.0, 0.0]))


def scan_left(*args, **kwargs):
    v.signal_animation_finished.disconnect()

    v.animate(high, low, scan, duration=2000, steps=60)
    v.signal_animation_finished.connect(scan_right)


def scan_right(*args, **kwargs):
    v.signal_animation_finished.disconnect()

    v.animate(low, high, scan, duration=2000, steps=60)
    v.signal_animation_finished.connect(scan_left)


# Hack to disconnect before starting
v.signal_animation_finished.connect(lambda: None)

# Mark all meshes and blocks as cross-sectionable
v.set_cross_section(True)

# Add the same mesh and block model, but without cross-sectioning, for comparison
v.load_mesh(mesh_path, color=[1.0, 0.8, 0.0], alpha=0.3)
v.load_blocks(block_path, alpha=0.3)

# Start animation
scan_right()

# Show viewer
v.show()
