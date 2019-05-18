#!/usr/bin/env python

import sys
import argparse


def application():
    from PyQt5.QtWidgets import QApplication
    from View.GUI.minevis import MineVis

    qt_app = QApplication(sys.argv)

    w = MineVis()
    w.show()

    sys.exit(qt_app.exec_())


def standalone():
    from View.standaloneviewer import viewer

    viewer.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Starts MineVis in app or standalone viewer mode.')
    parser.add_argument('--app', action='store_true', help='Starts in App mode.')
    parser.add_argument('--viewer', action='store_true', help='Starts in Viewer mode.')

    args = parser.parse_args()

    if args.viewer and not args.app:
        standalone()
    elif args.app or not args.viewer:
        application()
