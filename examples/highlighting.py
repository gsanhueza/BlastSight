#!/usr/bin/env python

from blastsight.view.viewer import Viewer

viewer = Viewer()
viewer.mesh_by_path('../test_files/blastsight.off', highlight=True)

viewer.fit_to_screen()
viewer.show()
