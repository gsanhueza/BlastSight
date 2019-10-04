#!/usr/bin/env python

from caseron.view.viewer import Viewer

v = Viewer()
v.mesh_by_path('../test_files/caseron.off')
v.signal_mesh_clicked.connect(lambda x: print(f'Attributes list: {x}'))

input('--- Double click on a mesh, read the attributes in the terminal. Enter to continue. ---\n')

v.fit_to_screen()
v.show()
