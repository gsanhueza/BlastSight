#!/usr/bin/env python

from View.standaloneviewer import StandaloneViewer
from View.Drawables.linegl import LineGL
from Model.Elements.lineelement import LineElement


if __name__ == '__main__':
    viewer = StandaloneViewer()
    # line = LineElement(x=[-1, 1], y=[0, 0], z=[0, 0], color=[0.0, 1.0, 0.0])
    line = LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 1.0, 0.0])

    drawable = viewer.add_drawable(line, LineGL)
    viewer.show()
