#!/usr/bin/env python

import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog
from qtpy import uic


class DialogCameraPosition(QDialog):
    def __init__(self, parent=None, drawable=None):
        QDialog.__init__(self, parent)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)

        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/dialogcameraposition.ui', self)
        self.parent = parent
        self.drawable = drawable

        self.setWindowTitle(f'Set camera position')

    def accept(self):
        self.parent.viewer.camera_position = [self.doubleSpinBox_x.value(),
                                              self.doubleSpinBox_y.value(),
                                              self.doubleSpinBox_z.value()]

        super().accept()

    def show(self):
        positions = self.parent.viewer.camera_position
        self.doubleSpinBox_x.setValue(positions[0])
        self.doubleSpinBox_y.setValue(positions[1])
        self.doubleSpinBox_z.setValue(positions[2])

        super().show()
