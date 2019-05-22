#!/usr/bin/env python

from View.standaloneviewer import StandaloneViewer

if __name__ == '__main__':
    viewer = StandaloneViewer()

    mesh_id = viewer.mesh_by_path('tests/Files/caseron.off')
    viewer.toggle_wireframe(mesh_id)
    viewer.block_model(x=[0, 5, 10], y=[0, 5, 10], z=[0, 0, 0], values=[5, 10, 15])
    viewer.show()
