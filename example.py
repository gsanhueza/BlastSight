#!/usr/bin/env python

from minevis.view.viewer import Viewer


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

    blocks = viewer.blocks(x=[-3, 3, 0],
                           y=[0, 0, 5],
                           z=[0, 0, 0],
                           block_size=[1.0, 1.0, 1.0],
                           values=[0.5, 1.0, 1.5])

    points_square = viewer.points(vertices=[[-3, 2, 0],
                                            [0, 2, 1],
                                            [3, 2, 0]],
                                  point_size=3.0,
                                  color=[[1.0, 1.0, 0.0],
                                         [0.0, 1.0, 1.0],
                                         [1.0, 0.0, 1.0]],
                                  marker='square')

    points_circle = viewer.points(vertices=[[-2, 3, 1],
                                            [0, 3, 0],
                                            [2, 3, 1]],
                                  point_size=[1, 3, 5],
                                  color=[[1.0, 0.0, 0.0],
                                         [0.0, 1.0, 0.0],
                                         [0.0, 0.0, 1.0]],
                                  marker='circle')

    lines = viewer.lines(x=[-0.5, 0.5],
                         y=[-2.0, 1.5],
                         z=[-2.0, -2.0],
                         color=[0.2, 0.8, 0.8])

    tubes = viewer.tubes(x=[0.5, -0.5, 1.5, 1.5],
                         y=[-2.0, 1.8, 1.8, 0.0],
                         z=[-1.5, -1.5, -1.5, -1.5],
                         color=[0.9, 0.2, 0.2],
                         radius=0.2,
                         resolution=150)

    viewer.camera_position = [0.0, 2.0, 15.0]
    viewer.centroid = [0.0, 0.0, 0.0]

    for id_, drawable in viewer.drawable_collection.items():
        print(f'Drawable {id_}: Name = {drawable.element.name}, Type = {type(drawable)}')

    viewer.show()
