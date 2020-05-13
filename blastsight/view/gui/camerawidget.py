#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget

from blastsight.view.gui.tools import uic


class CameraWidget(QWidget):
    signal_camera_translated = Signal(object)
    signal_camera_rotated = Signal(object)
    signal_center_translated = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/camerawidget.ui', self)

        # Avoids the QObject::startTimer warning (maybe)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._connect_internal_signals()

    def _connect_internal_signals(self) -> None:
        self.doubleSpinBox_x.valueChanged.connect(self.signal_camera_translated.emit)
        self.doubleSpinBox_y.valueChanged.connect(self.signal_camera_translated.emit)
        self.doubleSpinBox_z.valueChanged.connect(self.signal_camera_translated.emit)

        self.doubleSpinBox_rot_x.valueChanged.connect(self.signal_camera_rotated.emit)
        self.doubleSpinBox_rot_y.valueChanged.connect(self.signal_camera_rotated.emit)
        self.doubleSpinBox_rot_z.valueChanged.connect(self.signal_camera_rotated.emit)

        self.doubleSpinBox_center_x.valueChanged.connect(self.signal_center_translated.emit)
        self.doubleSpinBox_center_y.valueChanged.connect(self.signal_center_translated.emit)
        self.doubleSpinBox_center_z.valueChanged.connect(self.signal_center_translated.emit)

    def connect_viewer(self, viewer) -> None:
        # Connect viewer's signals to automatically update self
        viewer.signal_camera_rotated.connect(self.set_rotation_angle)
        viewer.signal_camera_translated.connect(self.set_camera_position)
        viewer.signal_center_translated.connect(self.set_rotation_center)

        # Connect signals to automatically update the viewer
        def angle_setter():
            viewer.rotation_angle = self.get_rotation_angle()

        def camera_setter():
            viewer.camera_position = self.get_camera_position()

        def center_setter():
            viewer.rotation_center = self.get_rotation_center()

        self.signal_camera_rotated.connect(angle_setter)
        self.signal_camera_translated.connect(camera_setter)
        self.signal_center_translated.connect(center_setter)

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
        self.blockSignals(True)
        self.doubleSpinBox_x.setValue(position[0])
        self.doubleSpinBox_y.setValue(position[1])
        self.doubleSpinBox_z.setValue(position[2])
        self.blockSignals(False)

    def set_rotation_angle(self, angle: list) -> None:
        self.blockSignals(True)
        self.doubleSpinBox_rot_x.setValue(angle[0])
        self.doubleSpinBox_rot_y.setValue(angle[1])
        self.doubleSpinBox_rot_z.setValue(angle[2])
        self.blockSignals(False)

    def set_rotation_center(self, center: list) -> None:
        self.blockSignals(True)
        self.doubleSpinBox_center_x.setValue(center[0])
        self.doubleSpinBox_center_y.setValue(center[1])
        self.doubleSpinBox_center_z.setValue(center[2])
        self.blockSignals(False)
