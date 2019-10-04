#!/usr/bin/env python

from caseron.view.viewer import Viewer

viewer = Viewer()
viewer.mesh_by_path('../test_files/caseron.off', highlight=True)

viewer.fit_to_screen()
viewer.show()
