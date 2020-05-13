#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtWidgets import *


class CameraWidget(QWidget):
    signal_camera_translated = Signal(object)
    signal_camera_rotated = Signal(object)
    signal_center_translated = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Camera Properties')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.label_position = QLabel('Camera position (X, Y, Z)', self)
        self.label_center = QLabel('Rotation angle (X°, Y°, Z°)', self)
        self.label_rotation = QLabel('Rotation center (X, Y, Z)', self)

        self.doubleSpinBox_x = self._generate_spinbox()
        self.doubleSpinBox_y = self._generate_spinbox()
        self.doubleSpinBox_z = self._generate_spinbox()

        self.doubleSpinBox_center_x = self._generate_spinbox()
        self.doubleSpinBox_center_y = self._generate_spinbox()
        self.doubleSpinBox_center_z = self._generate_spinbox()

        self.doubleSpinBox_rot_x = self._generate_spinbox(0, 360)
        self.doubleSpinBox_rot_y = self._generate_spinbox(0, 360)
        self.doubleSpinBox_rot_z = self._generate_spinbox(0, 360)

        # Layouts
        self.horizontal_position = QHBoxLayout()
        self.horizontal_center = QHBoxLayout()
        self.horizontal_rotation = QHBoxLayout()

        self.horizontal_position.addWidget(self.doubleSpinBox_x)
        self.horizontal_position.addWidget(self.doubleSpinBox_y)
        self.horizontal_position.addWidget(self.doubleSpinBox_z)

        self.horizontal_center.addWidget(self.doubleSpinBox_center_x)
        self.horizontal_center.addWidget(self.doubleSpinBox_center_y)
        self.horizontal_center.addWidget(self.doubleSpinBox_center_z)

        self.horizontal_rotation.addWidget(self.doubleSpinBox_rot_x)
        self.horizontal_rotation.addWidget(self.doubleSpinBox_rot_y)
        self.horizontal_rotation.addWidget(self.doubleSpinBox_rot_z)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label_position)
        self.layout.addLayout(self.horizontal_position)

        self.layout.addWidget(self.label_center)
        self.layout.addLayout(self.horizontal_center)

        self.layout.addWidget(self.label_rotation)
        self.layout.addLayout(self.horizontal_rotation)

        self._connect_internal_signals()

    def _generate_spinbox(self, lower: float = -9999999.9, upper: float = +9999999.9) -> QAbstractSpinBox:
        spinbox = QDoubleSpinBox(self)
        spinbox.setMinimum(lower)
        spinbox.setMaximum(upper)

        return spinbox

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

        # Fill the widget with viewer attributes
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
