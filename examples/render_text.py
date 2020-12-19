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

    # Setup our text
    viewer.register_drawable(TextGL(text="Hello", position=[0.0, 0.0, 180.0]))

    viewer.show()


if __name__ == '__main__':
    demo_text()
