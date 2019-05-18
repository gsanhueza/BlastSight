#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.GUI.mainwindow import MainWindow
from Model.model import Model

if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = Model()
    # model.mesh_by_path('tests/Files/caseron.off')
    window = MainWindow()
    window.set_model(model)

    window.show()
    sys.exit(app.exec_())
