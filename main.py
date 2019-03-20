#!/usr/bin/env python

import sys
from PySide2.QtWidgets import QApplication, QWidget

from mainwindow import MainWindow


if __name__ == "__main__":
    # Qt Application
    qt_app = QApplication(sys.argv)

    # MainWindow using QWidget as central widget
    widget = QWidget()
    window = MainWindow(widget)

    window.show()
    sys.exit(qt_app.exec_())
