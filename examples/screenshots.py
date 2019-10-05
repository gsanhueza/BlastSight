#!/usr/bin/env python

from blastsight.view.viewer import Viewer

v = Viewer()

v.mesh_by_path('../test_files/blastsight.off')
v.fit_to_screen()
v.resize(800, 800)

for i in range(3):
    #v.show(detached=True, timer=100)  # Optional
    v.take_screenshot(f'screenshot_{i}.png')
    v.rotation_angle += [0.0, 120.0, 0.0]
    #v.close()  # Optional

print('Ready!')
