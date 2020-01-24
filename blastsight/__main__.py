#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import argparse
import sys


def application(paths: list) -> None:
    from qtpy.QtWidgets import QApplication
    from blastsight.view.gui.mainwindow import MainWindow

    qt_app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    for path in paths:
        w.viewer.mesh_by_path(path)

    sys.exit(qt_app.exec_())


def container(paths: list) -> None:
    from qtpy.QtWidgets import QApplication
    from blastsight.view.gui.container import Container

    qt_app = QApplication(sys.argv)

    w = Container()
    w.show()

    for path in paths:
        w.viewer.mesh_by_path(path)

    sys.exit(qt_app.exec_())


def viewer(paths: list) -> None:
    from blastsight.view.viewer import Viewer
    v = Viewer()

    for path in paths:
        v.mesh_by_path(path)

    v.show()


def main() -> None:
    parser = argparse.ArgumentParser(description='Starts BlastSight in App/Container/Viewer mode.')
    parser.add_argument('-a', '--app', action='store_true', help='Starts in App mode.')
    parser.add_argument('-c', '--container', action='store_true', help='Starts in Container mode.')
    parser.add_argument('-v', '--viewer', action='store_true', help='Starts in Viewer mode.')
    parser.add_argument('paths', nargs='*', help='Paths of meshes loaded before opening BlastSight.')

    args = parser.parse_args()

    if args.viewer:
        viewer(args.paths)
    elif args.container:
        container(args.paths)
    else:
        application(args.paths)


if __name__ == '__main__':
    main()
