#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
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

    # Auto-load files when called from CLI or using "Open with..." from OS
    w.viewer.load_multiple(paths, w.viewer.load_mesh)

    sys.exit(qt_app.exec_())


def container(paths: list) -> None:
    from qtpy.QtWidgets import QApplication
    from blastsight.view.gui.container import Container

    qt_app = QApplication(sys.argv)

    w = Container()

    # Activate auto-fit
    if not w.toolbar.action_collection.action_autofit.isChecked():
        w.toolbar.action_collection.action_autofit.trigger()

    w.show()

    # Auto-load files when called from CLI
    w.viewer.load_multiple(paths, w.viewer.load_mesh)

    sys.exit(qt_app.exec_())


def viewer(paths: list) -> None:
    from blastsight.view.viewer import Viewer
    v = Viewer()

    # Auto-load files when called from CLI
    v.load_multiple(paths, v.load_mesh)

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
