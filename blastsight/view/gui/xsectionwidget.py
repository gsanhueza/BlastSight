#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtWidgets import *


class XSectionWidget(QWidget):
    signal_controller_requested = Signal(bool)
    signal_status_altered = Signal(bool)
    signal_phantom_altered = Signal(bool)

    signal_origin_altered = Signal(object)
    signal_normal_altered = Signal(object)
    signal_step_applied = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Cross-section properties')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Status buttons
        self.pushButton_controller = QPushButton('Slice from screen')
        self.pushButton_controller.setCheckable(True)

        self.pushButton_status = QPushButton('Show/Hide cross-section')
        self.pushButton_status.setCheckable(True)

        self.pushButton_phantom = QPushButton('Show/Hide phantom')
        self.pushButton_phantom.setCheckable(True)

        # Origin
        self.origin_x = self._generate_spinbox()
        self.origin_y = self._generate_spinbox()
        self.origin_z = self._generate_spinbox()

        # Normal
        self.normal_x = self._generate_spinbox(-1, +1, decimals=5, step=0.01)
        self.normal_y = self._generate_spinbox(-1, +1, decimals=5, step=0.01)
        self.normal_z = self._generate_spinbox(-1, +1, decimals=5, step=0.01)

        # Step
        self.step = self._generate_spinbox(lower=0.0)
        self.button_minus = self._generate_button('-')
        self.button_plus = self._generate_button('+')

        # Layout
        self.container = QWidget(self)
        self.grid = QGridLayout(self.container)
        self._add_to_grid(self.grid, 0, QLabel('Origin'), self.origin_x, self.origin_y, self.origin_z)
        self._add_to_grid(self.grid, 1, QLabel('Normal'), self.normal_x, self.normal_y, self.normal_z)
        self._add_to_grid(self.grid, 2, QLabel('Step'), self.step, self.button_minus, self.button_plus)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self._generate_horizontal(self.pushButton_controller,
                                                        self.pushButton_status,
                                                        self.pushButton_phantom))
        self.layout.addWidget(self.container)

        self._connect_internal_signals()

    def _generate_horizontal(self, *widgets) -> QWidget:
        container = QWidget(self)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        for widget in widgets:
            layout.addWidget(widget)

        return container

    @staticmethod
    def _add_to_grid(layout: QGridLayout, row: int, *widgets) -> None:
        for col, widget in enumerate(widgets):
            layout.addWidget(widget, row, col)

    def _generate_button(self, text: str, auto_repeat: bool = True) -> QAbstractButton:
        button = QPushButton(text, self)
        button.setAutoRepeat(auto_repeat)

        return button

    def _generate_spinbox(self, lower: float = -10e6, upper: float = 10e6,
                          decimals: int = 2, step: float = 1.0) -> QAbstractSpinBox:
        spinbox = QDoubleSpinBox(self)
        spinbox.setMinimum(lower)
        spinbox.setMaximum(upper)
        spinbox.setDecimals(decimals)
        spinbox.setSingleStep(step)
        spinbox.setMinimumWidth(10)

        return spinbox

    def _connect_internal_signals(self) -> None:
        self.pushButton_controller.clicked.connect(self.signal_controller_requested.emit)
        self.pushButton_status.clicked.connect(self.signal_status_altered.emit)
        self.pushButton_phantom.clicked.connect(self.signal_phantom_altered.emit)

        self.button_plus.clicked.connect(lambda: self.signal_step_applied.emit(+1))
        self.button_minus.clicked.connect(lambda: self.signal_step_applied.emit(-1))

        self.origin_x.valueChanged.connect(self.signal_origin_altered.emit)
        self.origin_y.valueChanged.connect(self.signal_origin_altered.emit)
        self.origin_z.valueChanged.connect(self.signal_origin_altered.emit)

        self.normal_x.valueChanged.connect(self.signal_normal_altered.emit)
        self.normal_y.valueChanged.connect(self.signal_normal_altered.emit)
        self.normal_z.valueChanged.connect(self.signal_normal_altered.emit)

    def connect_viewer(self, viewer) -> None:
        # Initialize self
        self.set_status(viewer.is_cross_sectioned)
        self.set_origin(viewer.last_cross_origin.tolist())
        self.set_normal(viewer.last_cross_normal.tolist())
        self.set_step(1.0)

        # Connect viewer's signals to automatically update self
        def handle_xsection_updated() -> None:
            self.set_origin(viewer.last_cross_origin.tolist())
            self.set_normal(viewer.last_cross_normal.tolist())
            self.set_status(viewer.is_cross_sectioned)
            self.set_phantom(viewer.is_phantom_enabled)

        # Connect signals to automatically update the viewer
        def handle_direction(direction: int) -> None:
            normal = viewer.last_cross_normal

            movement = direction * normal * self.get_step()
            origin = viewer.last_cross_origin + movement

            self.set_origin(origin)
            viewer.cross_section(origin, normal)

        # Connect controller
        def handle_screen_xsection(description: dict) -> None:
            # Retrieve description vectors
            origin = description.get('origin')
            normal = description.get('normal')
            up = description.get('up')

            self.signal_status_altered.emit(True)
            viewer.cross_section(origin, normal)
            viewer.set_camera_from_vectors(normal, up)

            # Auto-pop button after cross-sectioning from screen
            self.pushButton_controller.setChecked(False)
            handle_controller(False)

        def handle_controller(status: bool) -> None:
            if status:
                viewer.set_slice_controller()
                viewer.signal_slice_description.connect(handle_screen_xsection)
            else:
                viewer.set_normal_controller()

        # Connect signals
        viewer.signal_xsection_updated.connect(handle_xsection_updated)

        self.signal_controller_requested.connect(handle_controller)
        self.signal_status_altered.connect(viewer.set_cross_section)
        self.signal_phantom_altered.connect(viewer.set_phantom)

        self.signal_step_applied.connect(handle_direction)
        self.signal_origin_altered.connect(
            lambda *args: viewer.cross_section(self.get_origin(), self.get_normal()))
        self.signal_normal_altered.connect(
            lambda *args: viewer.cross_section(self.get_origin(), self.get_normal()))

    def get_status(self) -> bool:
        return self.pushButton_status.isChecked()

    def get_origin(self) -> list:
        return [self.origin_x.value(),
                self.origin_y.value(),
                self.origin_z.value()]

    def get_normal(self) -> list:
        return [self.normal_x.value(),
                self.normal_y.value(),
                self.normal_z.value()]

    def get_step(self) -> list:
        return self.step.value()

    def set_status(self, value: bool) -> None:
        self.blockSignals(True)
        self.pushButton_status.setChecked(value)
        self.blockSignals(False)

    def set_phantom(self, value: bool) -> None:
        self.blockSignals(True)
        self.pushButton_phantom.setChecked(value)
        self.blockSignals(False)

    def set_origin(self, value: list) -> None:
        self.blockSignals(True)
        self.origin_x.setValue(value[0])
        self.origin_y.setValue(value[1])
        self.origin_z.setValue(value[2])
        self.blockSignals(False)

    def set_normal(self, value: list) -> None:
        self.blockSignals(True)
        self.normal_x.setValue(value[0])
        self.normal_y.setValue(value[1])
        self.normal_z.setValue(value[2])
        self.blockSignals(False)

    def set_step(self, value: float) -> None:
        self.blockSignals(True)
        self.step.setValue(value)
        self.blockSignals(False)
