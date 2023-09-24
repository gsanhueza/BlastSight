#!/usr/bin/env python

import pathlib

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show how you can measure mesh distances from the viewer.
"""

v = Viewer()
title = v.windowTitle()

v.setWindowTitle(f'{title} - Click two points of a mesh.')

path = f'{pathlib.Path(__file__).parent.parent}/test_files/caseron.off'
mesh = v.load_mesh(path, color=[0.0, 0.3, 1.0])

phantom_tube = v.tubes(vertices=[mesh.center, mesh.center],
                       color=[1.0, 0.8, 0.0],
                       visible=False)


def update_info(d: dict):
    print(f'Distance dictionary: {d}')
    distance = d.get('distance')
    v.setWindowTitle(f'{title} - Distance: {distance}')

    points = [d.get('point_a'), d.get('point_b')]
    if distance is None:
        phantom_tube.is_visible = False
    else:
        phantom_tube.vertices = points
        phantom_tube.is_visible = True
        v.update_drawable(phantom_tube.id)


"""
Measurement mode enables you to click two points of a mesh
and measure the distance between those points.

Keep in mind that while in this mode, you cannot move/rotate the mesh,
but you can use the scroll wheel to zoom in/zoom out.
"""
v.set_measurement_interactor()
v.signal_mesh_distances.connect(update_info)

v.fit_to_screen()
v.show()
