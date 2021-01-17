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

    # Get some positions
    pos_min = min_bound
    pos_max = [min_bound[0], max_bound[0], min_bound[2]]

    # Setup our text
    viewer.text(text=f'.y = {str(round(min_bound[0], 3))}', position=pos_min)
    viewer.text(text=f'.y = {str(round(max_bound[1], 3))}', position=pos_max)
    viewer.lines(vertices=[pos_min, pos_max], color=[1.0, 0.0, 0.0], thickness=20)

    viewer.show()


if __name__ == '__main__':
    demo_text()
