#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
from View.mainwindow import MainWindow
from Model.model import Model


if __name__ == "__main__":
    import sys

    # Qt Application
    qt_app = QApplication(sys.argv)

    model = Model()
    window = MainWindow(model)

    window.show()
    sys.exit(qt_app.exec_())
