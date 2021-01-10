#!/usr/bin/env python

import pathlib

from blastsight.view.viewer import Viewer
from blastsight.view.drawables.textgl import TextGL

"""
In this demo, we'll show how to render simple text in BlastSight.
"""


def demo_text():
    viewer = Viewer()
    viewer.setWindowTitle('BlastSight (Text demo)')

    # Setup our text
    # viewer.register_drawable(TextGL(text="Hello world", position=[0.0, 0.0, 100.0], name='Hello', id=10))
    # viewer.register_drawable(TextGL(text="Guten Tag", position=[0.0, 100.0, 0.0], name='Guten', id=20))
    # viewer.register_drawable(TextGL(text="Bonjour", position=[100.0, 0.0, 0.0], name='Bonjour', id=30))

    path = f'{pathlib.Path(__file__).parent.parent}/test_files/caseron.off'
    mesh = viewer.load_mesh(path, color=[1.0, 1.0, 0.0], alpha=0.1)
    min_bound, max_bound = mesh.bounding_box
    viewer.register_drawable(TextGL(text=f".y = {str(round(min_bound[0], 3))}", position=min_bound, id=35))
    viewer.register_drawable(TextGL(text=f".y = {str(round(max_bound[1], 3))}", position=[min_bound[0], max_bound[0], min_bound[2]], id=36))
    viewer.lines(vertices=[min_bound, [min_bound[0], max_bound[0], min_bound[2]]], color=[1.0, 0.0, 0.0], thickness=20)

    viewer.show()


if __name__ == '__main__':
    demo_text()
