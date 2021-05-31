#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtWidgets import *


class GridWidget(QWidget):
    signal_visibility_altered = Signal(bool)
    signal_origin_altered = Signal(object)
    signal_length_altered = Signal(object)
    signal_separation_altered = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Grid properties')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Status button
        self.checkbox_visibility = QCheckBox()

        # Line separation
        self.separation = self._generate_spinbox(lower=1, step=1)

        # Origin
        self.origin_x = self._generate_spinbox()
        self.origin_y = self._generate_spinbox()
        self.origin_z = self._generate_spinbox()

        # Normal
        self.length_x = self._generate_spinbox(lower=0, decimals=0, step=1)
        self.length_y = self._generate_spinbox(lower=0, decimals=0, step=1)
        self.length_z = self._generate_spinbox(lower=0, decimals=0, step=1)

        # Layout
        self.container = QWidget(self)
        self.grid = QGridLayout(self.container)
        self._add_to_grid(self.grid, 0, QLabel('Grid visibility'), self.checkbox_visibility, QLabel('Line separation'), self.separation)
        self._add_to_grid(self.grid, 1, QLabel('Start position'), self.origin_x, self.origin_y, self.origin_z)
        self._add_to_grid(self.grid, 2, QLabel('Grid length'), self.length_x, self.length_y, self.length_z)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.container)

        self._connect_internal_signals()

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
        self.checkbox_visibility.clicked.connect(self.signal_visibility_altered.emit)
        self.separation.valueChanged.connect(self.signal_separation_altered.emit)

        def emit_origin(*args) -> None:
            self.signal_origin_altered.emit(self.get_origin())

        def emit_length(*args) -> None:
            self.signal_length_altered.emit(self.get_length())

        self.origin_x.valueChanged.connect(emit_origin)
        self.origin_y.valueChanged.connect(emit_origin)
        self.origin_z.valueChanged.connect(emit_origin)

        self.length_x.valueChanged.connect(emit_length)
        self.length_y.valueChanged.connect(emit_length)
        self.length_z.valueChanged.connect(emit_length)

    def connect_viewer(self, viewer) -> None:
        # Initialize self
        self.set_visibility(viewer.grid.is_visible)
        self.set_origin(viewer.last_cross_origin.tolist())
        self.set_length([10, 10, 10])
        self.set_separation(1)

        # Connect signals
        def handle_grid_visibility(status: bool) -> None:
            viewer.grid.is_visible = status

        def handle_grid_separation(value: float) -> None:
            viewer.grid.mark_separation = value
            viewer.makeCurrent()
            viewer.grid.setup_attributes()
            viewer.recreate()

        def handle_grid_origin(value: list) -> None:
            viewer.grid.origin = value
            viewer.makeCurrent()
            viewer.grid.reload()
            viewer.recreate()

        def handle_grid_length(value: list) -> None:
            viewer.grid.size = value
            viewer.makeCurrent()
            viewer.grid.reload()
            viewer.recreate()

        self.signal_visibility_altered.connect(handle_grid_visibility)
        self.signal_separation_altered.connect(handle_grid_separation)
        self.signal_origin_altered.connect(handle_grid_origin)
        self.signal_length_altered.connect(handle_grid_length)

    def get_visibility(self) -> bool:
        return self.checkbox_visibility.isChecked()

    def get_origin(self) -> list:
        return [self.origin_x.value(),
                self.origin_y.value(),
                self.origin_z.value()]

    def get_length(self) -> list:
        return [self.length_x.value(),
                self.length_y.value(),
                self.length_z.value()]

    def get_separation(self) -> list:
        return self.separation.value()

    def set_visibility(self, value: bool) -> None:
        self.blockSignals(True)
        self.checkbox_visibility.setChecked(value)
        self.blockSignals(False)

    def set_origin(self, value: list) -> None:
        self.blockSignals(True)
        self.origin_x.setValue(value[0])
        self.origin_y.setValue(value[1])
        self.origin_z.setValue(value[2])
        self.blockSignals(False)

    def set_length(self, value: list) -> None:
        self.blockSignals(True)
        self.length_x.setValue(value[0])
        self.length_y.setValue(value[1])
        self.length_z.setValue(value[2])
        self.blockSignals(False)

    def set_separation(self, value: float) -> None:
        self.blockSignals(True)
        self.separation.setValue(value)
        self.blockSignals(False)
