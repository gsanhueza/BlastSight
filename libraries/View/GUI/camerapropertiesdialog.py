#!/usr/bin/env python

import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog
from qtpy import uic


class CameraPropertiesDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/camerapropertiesdialog.ui', self)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.viewer = parent

    def accept(self):
        self.viewer.camera_position = [self.doubleSpinBox_x.value(),
                                       self.doubleSpinBox_y.value(),
                                       self.doubleSpinBox_z.value()]
        self.viewer.camera_rotation = [self.doubleSpinBox_rot_x.value(),
                                       self.doubleSpinBox_rot_y.value(),
                                       self.doubleSpinBox_rot_z.value()]
        self.viewer.centroid = [self.doubleSpinBox_center_x.value(),
                                self.doubleSpinBox_center_y.value(),
                                self.doubleSpinBox_center_z.value()]

        super().accept()

    def show(self):
        positions = self.viewer.camera_position
        rotations = self.viewer.camera_rotation
        centroid = self.viewer.centroid

        self.doubleSpinBox_x.setValue(positions[0])
        self.doubleSpinBox_y.setValue(positions[1])
        self.doubleSpinBox_z.setValue(positions[2])

        self.doubleSpinBox_rot_x.setValue(rotations[0])
        self.doubleSpinBox_rot_y.setValue(rotations[1])
        self.doubleSpinBox_rot_z.setValue(rotations[2])

        self.doubleSpinBox_center_x.setValue(centroid[0])
        self.doubleSpinBox_center_y.setValue(centroid[1])
        self.doubleSpinBox_center_z.setValue(centroid[2])

        super().show()
