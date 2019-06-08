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


def standalone():
    from libraries.View.standaloneviewer import StandaloneViewer
    viewer = StandaloneViewer()

    viewer.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Starts MineVis in App or standalone Viewer mode.')
    parser.add_argument('--app', action='store_true', help='Starts in App mode.')
    parser.add_argument('--viewer', action='store_true', help='Starts in Viewer mode.')

    args = parser.parse_args()

    if args.viewer and not args.app:
        standalone()
    elif args.app or not args.viewer:
        application()
