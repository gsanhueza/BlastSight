#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.openglwidget import OpenGLWidget


class MineVisViewer:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.widget = OpenGLWidget()

    def show(self):
        self.widget.show()
        return self.app.exec_()


if __name__ == '__main__':
    window = MineVisViewer()
    window.show()
