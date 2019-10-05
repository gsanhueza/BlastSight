#!/usr/bin/env python

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show how you can easily take screenshots of the viewer.
"""

v = Viewer()

v.mesh_by_path('../test_files/caseron.off')
v.fit_to_screen()
v.resize(800, 800)

"""
You can take a screenshot without even seeing the viewer,
but if you need to see it anyway, uncomment those "optional" lines.
"""

for i in range(3):
    # v.show(detached=True, timer=100)  # Optional
    v.take_screenshot(f'screenshot_{i}.png')
    v.rotation_angle += [0.0, 120.0, 0.0]
    # v.close()  # Optional

print('Ready!')
