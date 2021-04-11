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
    min_bound, max_bound = mesh.bounding_box
    lengths = max_bound - min_bound

    # Show a grid using the bounding box of the figure
    grid = viewer.grid(origin=min_bound, lengths=lengths, color=[1.0, 0.8, 0.0], mark_separation=10)

    # Labels in X
    # Remember to separate the number text from the grid
    for x in range(int(lengths[0] / grid.mark_separation) + 1):
        pos = min_bound[0] + x * grid.mark_separation
        viewer.text(text=f'{round(pos, 1)}', position=[pos, min_bound[1] - 2.0, min_bound[2]], scale=0.05)

    # Labels in Y
    for y in range(int(lengths[1] / grid.mark_separation) + 1):
        pos = min_bound[1] + y * grid.mark_separation
        viewer.text(text=f'{round(pos, 1)}', position=[min_bound[0] - 8.0, pos, min_bound[2] - 2.0], scale=0.05)

    # Labels in Z
    for z in range(int(lengths[2] / grid.mark_separation) + 1):
        pos = min_bound[2] + z * grid.mark_separation
        viewer.text(text=f'{round(pos, 1)}', position=[min_bound[0] - 8.0, min_bound[1], pos], scale=0.05)

    # Showcase orientations
    viewer.text(text='Facing: Elevation', position=mesh.center + [0.0, 0.0, 0.0], orientation='elevation')
    viewer.text(text='Facing: North', position=mesh.center + [0.0, 0.0, 3.0], orientation='north')
    viewer.text(text='Facing: East', position=mesh.center + [0.0, 5.0, 6.0], orientation='east')

    viewer.show()


if __name__ == '__main__':
    demo_text()
