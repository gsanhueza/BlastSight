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
    size = max_bound - min_bound
    mark_separation = 10

    viewer.grid.origin = min_bound
    viewer.grid.size = max_bound - min_bound
    viewer.grid.color = [1.0, 0.8, 0.0]
    viewer.grid.mark_separation = mark_separation
    viewer.grid.is_visible = True

    # Labels in X
    # Remember to separate the number text from the grid
    for x in range(int(size[0] / mark_separation) + 1):
        pos = min_bound[0] + x * mark_separation
        viewer.text(text=f'{round(pos, 1)}', position=[pos, min_bound[1] - 2.0, min_bound[2]], scale=0.05)

    # Labels in Y
    for y in range(int(size[1] / mark_separation) + 1):
        pos = min_bound[1] + y * mark_separation
        viewer.text(text=f'{round(pos, 1)}', position=[min_bound[0] - 8.0, pos, min_bound[2] - 2.0], scale=0.05)

    # Labels in Z
    for z in range(int(size[2] / mark_separation) + 1):
        pos = min_bound[2] + z * mark_separation
        viewer.text(text=f'{round(pos, 1)}', position=[min_bound[0] - 8.0, min_bound[1], pos], scale=0.05)

    # Showcase orientations
    viewer.text(text='Facing: Elevation', position=mesh.center + [0.0, 0.0, 0.0], orientation='elevation')
    viewer.text(text='Facing: North', position=mesh.center + [0.0, 0.0, 3.0], orientation='north')
    viewer.text(text='Facing: East', position=mesh.center + [0.0, 5.0, 6.0], orientation='east')

    viewer.show()


if __name__ == '__main__':
    demo_text()
