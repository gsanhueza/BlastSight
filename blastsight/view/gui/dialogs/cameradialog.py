#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog

from ..tools import uic


class CameraDialog(QDialog):
    def __init__(self, viewer=None):
        QDialog.__init__(self, viewer)
        uic.loadUi(f'{pathlib.Path(__file__).parent.parent}/UI/cameradialog.ui', self)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.connect_viewer(viewer)

    def connect_viewer(self, viewer) -> None:
        self.set_camera_position(viewer.get_camera_position())
        self.set_rotation_angle(viewer.get_rotation_angle())
        self.set_rotation_center(viewer.get_rotation_center())

    def get_camera_position(self) -> list:
        return [self.doubleSpinBox_x.value(),
                self.doubleSpinBox_y.value(),
                self.doubleSpinBox_z.value()]

    def get_rotation_angle(self) -> list:
        return [self.doubleSpinBox_rot_x.value(),
                self.doubleSpinBox_rot_y.value(),
                self.doubleSpinBox_rot_z.value()]

    def get_rotation_center(self) -> list:
        return [self.doubleSpinBox_center_x.value(),
                self.doubleSpinBox_center_y.value(),
                self.doubleSpinBox_center_z.value()]

    def set_camera_position(self, position: list) -> None:
        self.doubleSpinBox_x.setValue(position[0])
        self.doubleSpinBox_y.setValue(position[1])
        self.doubleSpinBox_z.setValue(position[2])

    def set_rotation_angle(self, angle: list) -> None:
        self.doubleSpinBox_rot_x.setValue(angle[0])
        self.doubleSpinBox_rot_y.setValue(angle[1])
        self.doubleSpinBox_rot_z.setValue(angle[2])

    def set_rotation_center(self, center: list) -> None:
        self.doubleSpinBox_center_x.setValue(center[0])
        self.doubleSpinBox_center_y.setValue(center[1])
        self.doubleSpinBox_center_z.setValue(center[2])
