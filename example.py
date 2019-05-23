#!/usr/bin/env python

from View.standaloneviewer import StandaloneViewer

if __name__ == '__main__':
    print('before creating StandaloneViewer()')
    viewer = StandaloneViewer()
    print('before adding a mesh')
    drawable = viewer.mesh_by_path('tests/Files/caseron.off')
    print('before trying to toggle the wireframe')
    drawable.toggle_wireframe()
    print('after trying to toggle the wireframe')
    viewer.show()
