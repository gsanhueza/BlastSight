#!/usr/bin/env python

from View.standaloneviewer import StandaloneViewer


if __name__ == '__main__':
    viewer = StandaloneViewer()

    mesh = viewer.mesh(x=[-1, 1, 0],
                       y=[0, 0, 1],
                       z=[0, 0, 0],
                       indices=[[0, 1, 2]])

    block = viewer.block_model(x=[-3, 3, 0],
                               y=[0, 0, 3],
                               z=[0, 0, 0],
                               values=[0.5, 1.0, 1.5])

    line = viewer.lines(x=[-0.5, 0.5],
                        y=[-2.0, 1.5],
                        z=[0.0, 0.0],
                        color=[0.2, 0.8, 0.8])
    viewer.show()
