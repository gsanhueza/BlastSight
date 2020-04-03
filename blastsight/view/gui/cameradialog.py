#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog
from .tools import uic


class CameraDialog(QDialog):
    def __init__(self, viewer=None):
        QDialog.__init__(self, viewer)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/cameradialog.ui', self)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.camera_position = viewer.camera_position
        self.rotation_angle = viewer.rotation_angle
        self.rotation_center = viewer.rotation_center

    @property
    def camera_position(self) -> list:
        return [self.doubleSpinBox_x.value(),
                self.doubleSpinBox_y.value(),
                self.doubleSpinBox_z.value()]

    @property
    def rotation_angle(self) -> list:
        return [self.doubleSpinBox_rot_x.value(),
                self.doubleSpinBox_rot_y.value(),
                self.doubleSpinBox_rot_z.value()]

    @property
    def rotation_center(self) -> list:
        return [self.doubleSpinBox_center_x.value(),
                self.doubleSpinBox_center_y.value(),
                self.doubleSpinBox_center_z.value()]

    @camera_position.setter
    def camera_position(self, position: list) -> None:
        self.doubleSpinBox_x.setValue(position[0])
        self.doubleSpinBox_y.setValue(position[1])
        self.doubleSpinBox_z.setValue(position[2])

    @rotation_angle.setter
    def rotation_angle(self, angle: list) -> None:
        self.doubleSpinBox_rot_x.setValue(angle[0])
        self.doubleSpinBox_rot_y.setValue(angle[1])
        self.doubleSpinBox_rot_z.setValue(angle[2])

    @rotation_center.setter
    def rotation_center(self, center: list) -> None:
        self.doubleSpinBox_center_x.setValue(center[0])
        self.doubleSpinBox_center_y.setValue(center[1])
        self.doubleSpinBox_center_z.setValue(center[2])
