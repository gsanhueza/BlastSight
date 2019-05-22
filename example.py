#!/usr/bin/env python

from View.standaloneviewer import StandaloneViewer

if __name__ == '__main__':
    print('A')
    viewer = StandaloneViewer()
    print('B')
    drawable = viewer.mesh_by_path('tests/Files/caseron.off')
    print('C')
    drawable.toggle_wireframe()
    print('D')
    viewer.show()
    print('E')

