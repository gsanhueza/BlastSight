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

    # Show an axis using the bounding box of the figure
    viewer.axis(origin=min_bound, lengths=max_bound - min_bound, color=[1.0, 0.8, 0.0])

    # Get some positions
    pos_x = [max_bound[0], min_bound[1], min_bound[2]]
    pos_y = [min_bound[0], max_bound[1], min_bound[2]]
    pos_z = [min_bound[0], min_bound[1], max_bound[2]]

    # Setup our text
    viewer.text(text=f'{pos_x}', position=pos_x)
    viewer.text(text=f'{pos_y}', position=pos_y)
    viewer.text(text=f'{pos_z}', position=pos_z)

    # Showcase orientations
    viewer.text(text='Facing: Elevation', position=[0.0, 0.0, 0.0], orientation='elevation')
    viewer.text(text='Facing: North', position=[0.0, 0.0, 3.0], orientation='north')
    viewer.text(text='Facing: East', position=[0.0, 5.0, 6.0], orientation='east')

    viewer.show()


if __name__ == '__main__':
    demo_text()
