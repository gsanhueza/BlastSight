#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import argparse
import sys


def application():
    from qtpy.QtWidgets import QApplication
    from blastsight.view.gui.mainwindow import MainWindow

    qt_app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(qt_app.exec_())


def container():
    from qtpy.QtWidgets import QApplication
    from blastsight.view.gui.container import Container

    qt_app = QApplication(sys.argv)

    w = Container()
    w.show()

    sys.exit(qt_app.exec_())


def viewer():
    from blastsight.view.viewer import Viewer
    v = Viewer()

    v.show()


def demo():
    from examples import demo
    demo.demo()


def main():
    parser = argparse.ArgumentParser(description='Starts BlastSight in App/Container/Viewer mode.')
    parser.add_argument('-a', '--app', action='store_true', help='Starts in App mode.')
    parser.add_argument('-c', '--container', action='store_true', help='Starts in Container mode.')
    parser.add_argument('-v', '--viewer', action='store_true', help='Starts in Viewer mode.')
    parser.add_argument('-d', '--demo', action='store_true', help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.viewer:
        viewer()
    elif args.container:
        container()
    elif args.demo:
        demo()
    else:
        application()


if __name__ == '__main__':
    main()
