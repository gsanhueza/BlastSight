#!/usr/bin/env python

import argparse
import sys


def application():
    from qtpy.QtWidgets import QApplication
    from minevis.view.gui.mainwindow import MainWindow

    qt_app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(qt_app.exec_())


def container():
    from qtpy.QtWidgets import QApplication
    from minevis.view.container import Container

    qt_app = QApplication(sys.argv)

    w = Container()
    w.show()

    sys.exit(qt_app.exec_())


def standalone():
    from minevis.view.viewer import Viewer
    viewer = Viewer()

    viewer.show()


def demo():
    from minevis.view.viewer import Viewer
    viewer = Viewer()
    viewer.setWindowTitle('MineVis (Demo)')

    viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[-3, -3, -3],
                color=[0.0, 0.0, 1.0],
                indices=[[0, 1, 2]],
                alpha=0.4,
                name='mesh_name',
                ext='dxf')

    viewer.blocks(x=[-3, 3, 0], y=[0, 0, 5], z=[0, 0, 0],
                  block_size=[1.0, 1.0, 1.0],
                  values=[0.5, 1.0, 1.5])

    viewer.points(vertices=[[-3, 2, 0], [0, 2, 1], [3, 2, 0]],
                  point_size=3.0,
                  color=[[1.0, 1.0, 0.0],
                         [0.0, 1.0, 1.0],
                         [1.0, 0.0, 1.0]],
                  marker='square')

    viewer.points(vertices=[[-2, 3, 1], [0, 3, 0], [2, 3, 1]],
                  point_size=[1, 3, 5],
                  color=[[1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, 0.0, 1.0]],
                  marker='circle')

    viewer.points(vertices=[[-3, 5, 0], [3, 5, 0]],
                  point_size=[4, 4],
                  color=[[0.8, 0.5, 0.2],
                         [0.5, 0.2, 0.8]],
                  marker='sphere')

    viewer.lines(x=[-0.5, 0.5], y=[-2.0, 1.5], z=[-2.0, -2.0],
                 color=[0.2, 0.8, 0.8])

    viewer.tubes(x=[0.5, -0.5, 1.5, 1.5], y=[-2.0, 1.8, 1.8, 0.0], z=[-1.5, -1.5, -1.5, -1.5],
                 color=[0.9, 0.2, 0.2],
                 radius=0.2,
                 resolution=150)

    viewer.camera_position = [0.0, 2.0, 15.0]
    viewer.centroid = [0.0, 0.0, 0.0]

    for id_, drawable in viewer.drawable_collection.items():
        print(f'Drawable {id_}: Name = {drawable.element.name}, Type = {type(drawable)}')

    viewer.show()


def main():
    parser = argparse.ArgumentParser(description='Starts MineVis in App/Container/Viewer mode.')
    parser.add_argument('-a', '--app', action='store_true', help='Starts in App mode.')
    parser.add_argument('-c', '--container', action='store_true', help='Starts in Container mode.')
    parser.add_argument('-v', '--viewer', action='store_true', help='Starts in Viewer mode.')
    parser.add_argument('-d', '--demo', action='store_true', help='Shows a demo of MineVis.')

    args = parser.parse_args()

    if args.viewer:
        standalone()
    elif args.container:
        container()
    elif args.demo:
        demo()
    else:
        application()


if __name__ == '__main__':
    main()
