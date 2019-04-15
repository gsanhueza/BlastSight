#!/usr/bin/env python

from PySide2.QtWidgets import QApplication
from View.mainwindow import MainWindow
from Model.model import Model


if __name__ == "__main__":
    import sys

    # Qt Application
    qt_app = QApplication(sys.argv)

    model = Model()
    window = MainWindow(model)

    # model.add_mesh('Model/Mesh/caseron.off')
    # model.add_mesh('Model/Mesh/caseron.dxf')
    # model.add_block_model('Model/BlockModel/mini.csv')

    window.show()
    sys.exit(qt_app.exec_())
