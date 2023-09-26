#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtGui import QColor
from qtpy.QtWidgets import *

from .customwidgets.coloredbutton import ColoredButton
from .customwidgets.colordialog import ColorDialog
from .customwidgets.doublespinbox import DoubleSpinBox
from .customwidgets.separatorframe import SeparatorFrame


class CameraWidget(QWidget):
    signal_camera_translated = Signal(object)
    signal_camera_rotated = Signal(object)
    signal_center_translated = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Viewer Properties')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.position_x = DoubleSpinBox(self)
        self.position_y = DoubleSpinBox(self)
        self.position_z = DoubleSpinBox(self)

        self.center_x = DoubleSpinBox(self)
        self.center_y = DoubleSpinBox(self)
        self.center_z = DoubleSpinBox(self)

        self.rotation_x = DoubleSpinBox(self, lower=-360, upper=360)
        self.rotation_y = DoubleSpinBox(self, lower=-360, upper=360)
        self.rotation_z = DoubleSpinBox(self, lower=-360, upper=360)

        self.button_top = ColoredButton(self, 'Top', (0.1, 0.2, 0.3, 1.0))
        self.button_bottom = ColoredButton(self, 'Bottom', (0.4, 0.5, 0.6, 1.0))

        self.current_interactor = QLabel(self)
        self.current_projection = QLabel(self)

        # Layouts
        self.layout = QVBoxLayout(self)

        self._add_to_layout(self.layout, [
            QLabel('Camera position (location)'),
            self._generate_horizontal(self.position_x, self.position_y, self.position_z),
            SeparatorFrame(self),

            QLabel('Rotation center (location)'),
            self._generate_horizontal(self.center_x, self.center_y, self.center_z),
            SeparatorFrame(self),

            QLabel('Rotation angle (degrees)'),
            self._generate_horizontal(self.rotation_x, self.rotation_y, self.rotation_z),
            SeparatorFrame(self),

            QLabel('Background color'),
            self._generate_horizontal(self.button_top, self.button_bottom),
            SeparatorFrame(self),

            self._generate_horizontal(QLabel('Interactor'), self.current_interactor),
            self._generate_horizontal(QLabel('Projection'), self.current_projection),
        ])

        self.layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self._connect_internal_signals()

    @staticmethod
    def _add_to_layout(layout, widgets: list) -> None:
        for widget in widgets:
            layout.addWidget(widget)

    def _generate_horizontal(self, *widgets) -> QWidget:
        container = QWidget(self)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        for widget in widgets:
            layout.addWidget(widget)

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

        viewer.signal_interactor_updated.connect(self.set_current_interactor)
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
        self.set_current_interactor(viewer.current_interactor.name)
        self.set_current_projection(viewer.current_projection)

        # Set-up initial colors
        self.button_top.set_color(viewer.background.top_color)
        self.button_bottom.set_color(viewer.background.bottom_color)

        # Connect button handlers
        self.button_bottom.clicked.connect(lambda *_: self.show_colordialog_bottom(viewer))
        self.button_top.clicked.connect(lambda *_: self.show_colordialog_top(viewer))

    def show_colordialog_bottom(self, viewer) -> None:
        def set_background_color(*_):
            self.button_bottom.set_qcolor(dialog.currentColor())
            viewer.background.bottom_color = self.button_bottom.get_color()
            viewer.update()

        dialog = ColorDialog()
        dialog.setCurrentColor(self.button_bottom.qcolor)
        dialog.accepted.connect(set_background_color)

        dialog.show()

    def show_colordialog_top(self, viewer) -> None:
        def set_background_color(*_):
            self.button_top.set_qcolor(dialog.currentColor())
            viewer.background.top_color = self.button_top.get_color()
            viewer.update()

        dialog = ColorDialog()
        dialog.setCurrentColor(self.button_top.qcolor)
        dialog.accepted.connect(set_background_color)
        dialog.show()

    """
    Getters/Setters
    """
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

    def set_current_interactor(self, mode: str) -> None:
        self.current_interactor.setText(mode)

    def set_current_projection(self, projection: str) -> None:
        self.current_projection.setText(projection)
