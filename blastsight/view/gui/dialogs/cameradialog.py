#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QDialog

from ..tools import uic


class CameraDialog(QDialog):
    signal_camera_translated = Signal(object)
    signal_camera_rotated = Signal(object)
    signal_center_translated = Signal(object)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent.parent}/UI/cameradialog.ui', self)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._connect_internal_signals()

    def _connect_internal_signals(self):
        self.doubleSpinBox_x.valueChanged.connect(self.signal_camera_translated.emit)
        self.doubleSpinBox_y.valueChanged.connect(self.signal_camera_translated.emit)
        self.doubleSpinBox_z.valueChanged.connect(self.signal_camera_translated.emit)

        self.doubleSpinBox_rot_x.valueChanged.connect(self.signal_camera_rotated.emit)
        self.doubleSpinBox_rot_y.valueChanged.connect(self.signal_camera_rotated.emit)
        self.doubleSpinBox_rot_z.valueChanged.connect(self.signal_camera_rotated.emit)

        self.doubleSpinBox_center_x.valueChanged.connect(self.signal_center_translated.emit)
        self.doubleSpinBox_center_y.valueChanged.connect(self.signal_center_translated.emit)
        self.doubleSpinBox_center_z.valueChanged.connect(self.signal_center_translated.emit)

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
