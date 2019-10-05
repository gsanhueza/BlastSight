#!/usr/bin/env python

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show how you can use the signals of the viewer.
"""

v = Viewer()
v.mesh_by_path('../test_files/caseron.off')

"""
For example, you may want to do something when we detect a clicked mesh.
For that, just connect the signal to your function/method.
Check IntegrableViewer's code to know which signals are available.
"""

v.signal_mesh_clicked.connect(lambda x: print(f'Attributes list: {x}'))

input('--- Double click on a mesh, read the attributes in the terminal. Enter to continue. ---\n')

v.fit_to_screen()
v.show()
