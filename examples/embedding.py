#!/usr/bin/env python

import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QLabel
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QGridLayout
from qtpy.QtWidgets import QOpenGLWidget
from qtpy.QtWidgets import QPushButton

from caseron.view.gui.container import Container


if __name__ == '__main__':
    app = QApplication(sys.argv)
    central_widget = QWidget()
    central_widget.setWindowTitle('Embedding MineVisGL in a PyQt5/PySide2 Application')
    layout = QGridLayout(central_widget)
    container = Container(central_widget)

    label_list = []
    for i in range(3):
        for j in range(3):
            if (i == j == 1):
                continue

            label = QLabel(central_widget)
            label.setText('Other QWidget at (%d, %d)' % (i,j))
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            layout.addWidget(label, i, j)
            label_list.append(label)

    layout.addWidget(container, 1, 1)

    window = QMainWindow()
    window.setCentralWidget(central_widget)
    window.show()

    app.exec_()
