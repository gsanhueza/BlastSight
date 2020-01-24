#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog
from qtpy import uic


class CameraDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/cameradialog.ui', self)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.viewer = parent

    def accept(self) -> None:
        self.viewer.camera_position = [self.doubleSpinBox_x.value(),
                                       self.doubleSpinBox_y.value(),
                                       self.doubleSpinBox_z.value()]
        self.viewer.rotation_angle = [self.doubleSpinBox_rot_x.value(),
                                      self.doubleSpinBox_rot_y.value(),
                                      self.doubleSpinBox_rot_z.value()]
        self.viewer.rotation_center = [self.doubleSpinBox_center_x.value(),
                                       self.doubleSpinBox_center_y.value(),
                                       self.doubleSpinBox_center_z.value()]

        super().accept()

    def show(self) -> None:
        positions = self.viewer.camera_position
        rotations = self.viewer.rotation_angle
        centers = self.viewer.rotation_center

        self.doubleSpinBox_x.setValue(positions[0])
        self.doubleSpinBox_y.setValue(positions[1])
        self.doubleSpinBox_z.setValue(positions[2])

        self.doubleSpinBox_rot_x.setValue(rotations[0])
        self.doubleSpinBox_rot_y.setValue(rotations[1])
        self.doubleSpinBox_rot_z.setValue(rotations[2])

        self.doubleSpinBox_center_x.setValue(centers[0])
        self.doubleSpinBox_center_y.setValue(centers[1])
        self.doubleSpinBox_center_z.setValue(centers[2])

        super().show()
