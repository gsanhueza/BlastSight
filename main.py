#!/usr/bin/env python

import argparse
import sys


def application():
    from qtpy.QtWidgets import QApplication
    from libraries.View.GUI.mainwindow import MineVis

    qt_app = QApplication(sys.argv)

    w = MineVis()
    w.show()

    sys.exit(qt_app.exec_())


def container():
    from qtpy.QtWidgets import QApplication
    from libraries.View.GUI.container import Container

    qt_app = QApplication(sys.argv)

    w = Container()
    w.show()

    sys.exit(qt_app.exec_())


def standalone():
    from libraries.View.viewer import Viewer
    viewer = Viewer()

    viewer.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Starts MineVis in App/Container/Viewer mode.')
    parser.add_argument('-a', '--app', action='store_true', help='Starts in App mode.')
    parser.add_argument('-c', '--container', action='store_true', help='Starts in Container mode.')
    parser.add_argument('-v', '--viewer', action='store_true', help='Starts in Viewer mode.')

    args = parser.parse_args()

    if args.viewer:
        standalone()
    elif args.container:
        container()
    else:
        application()
