#!/usr/bin/env python

from libraries.Model.tests.globals import *
from libraries.View.viewer import Viewer


if __name__ == '__main__':
    viewer = Viewer()

    mesh = viewer.mesh(x=[-1, 1, 0],
                       y=[0, 0, 1],
                       z=[-3, -3, -3],
                       color=[0.0, 0.0, 1.0],
                       indices=[[0, 1, 2]],
                       alpha=0.4,
                       name='mesh_name',
                       ext='dxf')

    mesh_p = viewer.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/caseron.off', color=[1.0, 0.0, 0.0])
    mesh_p.enable_wireframe()

    blocks = viewer.block_model(x=[-3, 3, 0],
                                y=[0, 0, 5],
                                z=[0, 0, 0],
                                block_size=[1.0, 1.0, 1.0],
                                values=[0.5, 1.0, 1.5])

    points = viewer.points(vertices=[[-3, 2, 0],
                                     [0, 2, 1],
                                     [3, 2, 2]],
                           point_size=3.0,
                           values=[1.5, 1.0, 0.5],
                           vmin=0.8,
                           vmax=2.0)

    lines = viewer.lines(x=[-0.5, 0.5],
                         y=[-2.0, 1.5],
                         z=[-2.0, -2.0],
                         color=[0.2, 0.8, 0.8])

    tubes = viewer.tubes(x=[0.5, -0.5, 1.5, 1.5],
                         y=[-2.0, 1.8, 1.8, 0.0],
                         z=[-1.5, -1.5, -1.5, -1.5],
                         color=[0.9, 0.2, 0.2],
                         radius=0.2,
                         resolution=15)

    viewer.camera_position = [0.0, 2.0, 15.0]
    viewer.centroid = [0.0, 0.0, 0.0]

    viewer.get_drawable('AXIS').hide()
    viewer.get_drawable('AXIS').show()

    for id_, drawable in viewer.drawable_collection.items():
        print(f'Drawable {id_}: Name = {drawable.element.name}, Type = {type(drawable)}')

    viewer.show()
