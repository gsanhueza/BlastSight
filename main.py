#!/usr/bin/env python

import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QGuiApplication

from View.mainwindow import MainWindow
from Model.model import Model


if __name__ == "__main__":
    # Qt Application
    QGuiApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    qt_app = QApplication(sys.argv)

    model = Model()
    window = MainWindow(model)

    window.show()
    sys.exit(qt_app.exec_())
