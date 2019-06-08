#!/usr/bin/env python

from libraries.Model.tests.globals import *
from libraries.View.standaloneviewer import StandaloneViewer


def main():
    viewer = StandaloneViewer()

    mesh = viewer.mesh(x=[-1, 1, 0],
                       y=[0, 0, 1],
                       z=[0, 0, 0],
                       color=[0.0, 0.0, 1.0],
                       indices=[[0, 1, 2]],
                       name='mesh_name')

    mesh_p = viewer.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/caseron.off', color=[1.0, 0.0, 0.0])
    mesh_p.enable_wireframe()

    block = viewer.block_model(x=[-3, 3, 0],
                               y=[0, 0, 5],
                               z=[0, 0, 0],
                               values=[0.5, 1.0, 1.5])

    lines = viewer.lines(x=[-0.5, 0.5],
                         y=[-2.0, 1.5],
                         z=[0.0, 0.0],
                         color=[0.2, 0.8, 0.8])

    tubes = viewer.tubes(x=[0.5, -0.5, 1.5, 1.5],
                         y=[-2.0, 1.8, 1.8, 0.0],
                         z=[0.0, 0.0, 0.0, 0.0],
                         radius=0.5,
                         resolution=8,
                         color=[0.9, 0.2, 0.2])

    viewer.camera_position = [0.0, 2.0, 15.0]

    for id_, drawable in viewer.drawable_collection.items():
        print(f'Drawable {id_}: Name = {drawable.element.name}')

    viewer.show()


if __name__ == '__main__':
    main()
