#!/usr/bin/env python

from View.standaloneviewer import StandaloneViewer
from View.Drawables.linegl import LineGL
from Model.Elements.lineelement import LineElement


if __name__ == '__main__':
    viewer = StandaloneViewer()
    line = LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[0.2, 0.8, 0.8])

    drawable = viewer.add_drawable(line, LineGL)
    viewer.show()
