#!/usr/bin/env python

from blastsight.view.viewer import Viewer
from blastsight.view.drawables.textgl import TextGL
from blastsight.model.elements.nullelement import NullElement

"""
In this demo, we'll show how to render simple text in BlastSight.
"""


def demo_text():
    viewer = Viewer()
    viewer.setWindowTitle('BlastSight (Text demo)')

    textgl = TextGL(NullElement(id=0))
    viewer.register_drawable(textgl, viewer.post_collection)

    # First letter should be here
    square = viewer.mesh(
        triangles=[
            [20.0, 79.0, 0.0],
            [20.0, 50.0, 0.0],
            [45.0, 50.0, 0.0],
            [20.0, 79.0, 0.0],
            [45.0, 50.0, 0.0],
            [45.0, 79.0, 0.0]],
        color=[1.0, 1.0, 1.0],
        wireframe=True,
    )

    square.show()
    viewer.show(autofit=False)


if __name__ == '__main__':
    demo_text()
