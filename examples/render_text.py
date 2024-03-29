#!/usr/bin/env python

import pathlib

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show how to render simple text in BlastSight.
"""


def demo_text():
    viewer = Viewer()
    viewer.setWindowTitle('BlastSight (Text demo)')

    # Load a mesh
    path = f'{pathlib.Path(__file__).parent.parent}/test_files/caseron.off'
    mesh = viewer.load_mesh(path, color=[1.0, 1.0, 0.0], alpha=0.1)

    # Setup the grid using the bounding box of the figure
    min_bound, max_bound = mesh.bounding_box

    viewer.grid.origin = min_bound
    viewer.grid.size = max_bound - min_bound
    viewer.grid.color = [1.0, 0.8, 0.0]
    viewer.grid.mark_separation = 10
    viewer.grid.is_visible = True

    # Showcase orientations
    viewer.text(text='Facing: Elevation', position=mesh.center, rotation=[0.0, 0.0, 0.0], scale=10)
    viewer.text(text='Facing: North', position=mesh.center, rotation=[0.0, 90.0, 90.0], scale=10)
    viewer.text(text='Facing: East', position=mesh.center, rotation=[90.0, 0.0, 0.0], scale=10)

    viewer.show()


if __name__ == '__main__':
    demo_text()
