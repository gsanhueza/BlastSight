#!/usr/bin/env python

from View.standaloneviewer import viewer

viewer.mesh_by_path('tests/Files/caseron.off')
viewer.hide_drawable(0)
viewer.show()
