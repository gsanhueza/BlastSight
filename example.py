#!/usr/bin/env python

from View.standaloneviewer import StandaloneViewer

if __name__ == '__main__':
    viewer = StandaloneViewer()

    drawable = viewer.mesh_by_path('tests/Files/caseron.off')
    drawable.toggle_wireframe()

    viewer.show()
