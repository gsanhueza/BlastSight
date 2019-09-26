#!/usr/bin/env python

import argparse
import sys


def application():
    from qtpy.QtWidgets import QApplication
    from caseron.view.gui.mainwindow import MainWindow

    qt_app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(qt_app.exec_())


def container():
    from qtpy.QtWidgets import QApplication
    from caseron.view.gui.container import Container

    qt_app = QApplication(sys.argv)

    w = Container()
    w.show()

    sys.exit(qt_app.exec_())


def standalone():
    from caseron.view.viewer import Viewer
    viewer = Viewer()

    viewer.show()


def demo():
    from caseron.view.viewer import Viewer
    viewer = Viewer()
    viewer.setWindowTitle('Caseron (Demo)')

    viewer.mesh(x=[1, 3, 2], y=[0, 0, 1], z=[-3, -3, -3],
                color=[0.0, 0.0, 1.0],
                indices=[[0, 1, 2]],
                alpha=0.7,
                name='Normal Mesh')

    viewer.mesh(x=[1, 3, 2], y=[0, 0, -1], z=[-3, -3, -3],
                color=[1.0, 0.5, 0.0],
                indices=[[0, 1, 2]],
                alpha=1.0,
                wireframe=True,
                name='Wireframed Mesh')

    viewer.mesh(x=[-3, -1, -2, -2], y=[0, 0, 1, -1], z=[-3, -3, -3, -3],
                color=[1.0, 0.5, 0.5],
                indices=[[0, 1, 2], [0, 3, 1]],
                alpha=1.0,
                highlight=True,
                name='Highlighted Mesh')

    viewer.blocks(x=[-4, 4, 0], y=[0, 0, 5], z=[0, 0, 0],
                  block_size=[1.0, 1.0, 1.0],
                  values=[0.5, 1.0, 1.5],
                  name='Blocks')

    viewer.points(vertices=[[-3, 2, 0], [0, 2, 1], [3, 2, 0]],
                  point_size=1.0,
                  color=[[1.0, 1.0, 0.0],
                         [0.0, 1.0, 1.0],
                         [1.0, 0.0, 1.0]],
                  marker='square',
                  name='Points rendered as squares')

    viewer.points(vertices=[[-2, 3, 1], [0, 3, 0], [2, 3, 1]],
                  point_size=[0.3, 0.6, 0.9],
                  color=[[1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, 0.0, 1.0]],
                  marker='circle',
                  name='Points rendered as circles')

    viewer.points(vertices=[[-3, 5, 0], [3, 5, 0]],
                  point_size=2.0,
                  color=[[0.8, 0.5, 0.2],
                         [0.5, 0.2, 0.8]],
                  marker='sphere',
                  name='Points rendered as spheres')

    viewer.lines(x=[-1.0, 1.0, -1.0, 1.0], y=[1.0, 1.0, -1.0, -1.0], z=[-2.0, -2.0, -2.0, -2.0],
                 color=[0.2, 0.8, 0.8],
                 loop=True,
                 name='Lines')

    viewer.tubes(x=[1.0, -1.0, 1.0, -1.0], y=[2.0, 2.0, -2.0, -2.0], z=[-1.5, -1.5, -1.5, -1.5],
                 color=[0.9, 0.2, 0.2],
                 radius=0.2,
                 resolution=150,
                 loop=False,
                 name='Tubes')

    viewer.fit_to_screen()
    viewer.camera_position += [0.0, 0.0, 5.0]

    for _id, drawable in viewer.drawable_collection.items():
        print(f'ID: {_id}\t Type: {type(drawable)}\t Name: {drawable.element.name}')

    viewer.show()


def main():
    parser = argparse.ArgumentParser(description='Starts Caseron in App/Container/Viewer mode.')
    parser.add_argument('-a', '--app', action='store_true', help='Starts in App mode.')
    parser.add_argument('-c', '--container', action='store_true', help='Starts in Container mode.')
    parser.add_argument('-v', '--viewer', action='store_true', help='Starts in Viewer mode.')
    parser.add_argument('-d', '--demo', action='store_true', help='Shows a demo of Caseron.')

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
