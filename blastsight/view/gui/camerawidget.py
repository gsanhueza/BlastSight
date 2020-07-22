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

        self.label_position = QLabel('Camera position (location)', self)
        self.label_center = QLabel('Rotation center (location)', self)
        self.label_rotation = QLabel('Rotation angle (degrees)', self)
        # self.label_background = QLabel('Background color (Top/Bottom)', self)

        self.position_x = self._generate_spinbox()
        self.position_y = self._generate_spinbox()
        self.position_z = self._generate_spinbox()

        self.center_x = self._generate_spinbox()
        self.center_y = self._generate_spinbox()
        self.center_z = self._generate_spinbox()

        self.rotation_x = self._generate_spinbox(-360, 360)
        self.rotation_y = self._generate_spinbox(-360, 360)
        self.rotation_z = self._generate_spinbox(-360, 360)

        # self.button_top = QPushButton('Top')
        # self.button_bottom = QPushButton('Bottom')

        self.current_mode = QLabel(self)
        self.current_projection = QLabel(self)

        self.vertical_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Layouts
        self.layout = QVBoxLayout(self)
        self.horizontal_position = QHBoxLayout()
        self.horizontal_center = QHBoxLayout()
        self.horizontal_rotation = QHBoxLayout()

        # Adapter for horizontal generation
        def adapter(layout):
            layout.setStretch(0, 1)
            layout.setStretch(1, 8)

        self.add_to_layout(self.layout, [
            self.label_position,
            self._generate_horizontal(QLabel('X'), self.position_x, adapter=adapter),
            self._generate_horizontal(QLabel('Y'), self.position_y, adapter=adapter),
            self._generate_horizontal(QLabel('Z'), self.position_z, adapter=adapter),
            self._generate_separator(),

            self.label_center,
            self._generate_horizontal(QLabel('X'), self.center_x, adapter=adapter),
            self._generate_horizontal(QLabel('Y'), self.center_y, adapter=adapter),
            self._generate_horizontal(QLabel('Z'), self.center_z, adapter=adapter),
            self._generate_separator(),

            self.label_rotation,
            self._generate_horizontal(QLabel('X°'), self.rotation_x, adapter=adapter),
            self._generate_horizontal(QLabel('Y°'), self.rotation_y, adapter=adapter),
            self._generate_horizontal(QLabel('Z°'), self.rotation_z, adapter=adapter),
            self._generate_separator(),

            # self.label_background,
            # self._generate_horizontal(self.button_top, self.button_bottom)
            # self._generate_separator(),

            self._generate_horizontal(QLabel('Mode'), self.current_mode),
            self._generate_horizontal(QLabel('Projection'), self.current_projection),
        ])

        self.layout.addSpacerItem(self.vertical_spacer)

        self._connect_internal_signals()

    @staticmethod
    def add_to_layout(layout, widgets: list) -> None:
        for widget in widgets:
            layout.addWidget(widget)

    def _generate_spinbox(self, lower: float = -10e6, upper: float = 10e6) -> QAbstractSpinBox:
        spinbox = QDoubleSpinBox(self)
        spinbox.setMinimum(lower)
        spinbox.setMaximum(upper)

        return spinbox

    def _generate_separator(self) -> QFrame:
        line_separator = QFrame(self)
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)

        return line_separator

    def _generate_horizontal(self, *widgets, **kwargs) -> QWidget:
        container = QWidget(self)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        for widget in widgets:
            # widget.set_parent(container)
            layout.addWidget(widget)

        # Execute layout adapter
        adapter = kwargs.get('adapter', lambda *args: None)
        adapter(layout)

        return container

    def _connect_internal_signals(self) -> None:
        self.position_x.valueChanged.connect(self.signal_camera_translated.emit)
        self.position_y.valueChanged.connect(self.signal_camera_translated.emit)
        self.position_z.valueChanged.connect(self.signal_camera_translated.emit)

        self.rotation_x.valueChanged.connect(self.signal_camera_rotated.emit)
        self.rotation_y.valueChanged.connect(self.signal_camera_rotated.emit)
        self.rotation_z.valueChanged.connect(self.signal_camera_rotated.emit)

        self.center_x.valueChanged.connect(self.signal_center_translated.emit)
        self.center_y.valueChanged.connect(self.signal_center_translated.emit)
        self.center_z.valueChanged.connect(self.signal_center_translated.emit)

    def connect_viewer(self, viewer) -> None:
        # Connect viewer's signals to automatically update self
        viewer.signal_camera_rotated.connect(self.set_rotation_angle)
        viewer.signal_camera_translated.connect(self.set_camera_position)
        viewer.signal_center_translated.connect(self.set_rotation_center)

        viewer.signal_mode_updated.connect(self.set_current_mode)
        viewer.signal_projection_updated.connect(self.set_current_projection)

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
        self.set_current_mode(viewer.current_mode.name)
        self.set_current_projection(viewer.projection_mode)

    def get_camera_position(self) -> list:
        return [self.position_x.value(),
                self.position_y.value(),
                self.position_z.value()]

    def get_rotation_angle(self) -> list:
        return [self.rotation_x.value(),
                self.rotation_y.value(),
                self.rotation_z.value()]

    def get_rotation_center(self) -> list:
        return [self.center_x.value(),
                self.center_y.value(),
                self.center_z.value()]

    def set_camera_position(self, position: list) -> None:
        self.blockSignals(True)
        self.position_x.setValue(position[0])
        self.position_y.setValue(position[1])
        self.position_z.setValue(position[2])
        self.blockSignals(False)

    def set_rotation_angle(self, angle: list) -> None:
        self.blockSignals(True)
        self.rotation_x.setValue(angle[0])
        self.rotation_y.setValue(angle[1])
        self.rotation_z.setValue(angle[2])
        self.blockSignals(False)

    def set_rotation_center(self, center: list) -> None:
        self.blockSignals(True)
        self.center_x.setValue(center[0])
        self.center_y.setValue(center[1])
        self.center_z.setValue(center[2])
        self.blockSignals(False)

    def set_current_mode(self, mode: str) -> None:
        self.current_mode.setText(mode)

    def set_current_projection(self, projection: str) -> None:
        self.current_projection.setText(projection)
