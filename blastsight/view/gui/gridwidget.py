#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtGui import QColor
from qtpy.QtWidgets import *

from colour import Color


class GridWidget(QWidget):
    signal_visibility_requested = Signal(bool)
    signal_grid_color_requested = Signal()
    signal_text_color_requested = Signal()

    signal_origin_altered = Signal(object)
    signal_length_altered = Signal(object)
    signal_separation_altered = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Grid properties')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Status button
        self.button_visibility = QPushButton('Hidden', self)
        self.button_visibility.setCheckable(True)

        # Color buttons
        self.button_grid_color = QPushButton('')  # Labels deliberately omitted
        self.button_text_color = QPushButton('')

        # Line separation
        self.separation = self._generate_spinbox(lower=1, step=1)

        # Origin
        self.origin_x = self._generate_spinbox()
        self.origin_y = self._generate_spinbox()
        self.origin_z = self._generate_spinbox()

        # Length
        self.length_x = self._generate_spinbox(lower=0, decimals=0, step=1)
        self.length_y = self._generate_spinbox(lower=0, decimals=0, step=1)
        self.length_z = self._generate_spinbox(lower=0, decimals=0, step=1)

        # Layout
        self.container = QWidget(self)
        self.grid = QGridLayout(self.container)
        self._add_to_grid(self.grid, 0,
                          QLabel('Grid visibility'), self.button_visibility,
                          QLabel('Line separation'), self.separation)
        self._add_to_grid(self.grid, 1,
                          QLabel('Grid color'), self.button_grid_color,
                          QLabel('Text color'), self.button_text_color)
        self._add_to_grid(self.grid, 2, QLabel('Grid origin'), self.origin_x, self.origin_y, self.origin_z)
        self._add_to_grid(self.grid, 3, QLabel('Grid length'), self.length_x, self.length_y, self.length_z)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.container)

        self._connect_internal_signals()

    @staticmethod
    def _get_button_stylesheet(color: list) -> str:
        return f'background-color: {Color(rgb=color[:3]).get_web()}; border: none;'

    @staticmethod
    def _add_to_grid(layout: QGridLayout, row: int, *widgets) -> None:
        for col, widget in enumerate(widgets):
            layout.addWidget(widget, row, col)

    def _generate_button(self, text: str, auto_repeat: bool = True) -> QAbstractButton:
        button = QPushButton(text, self)
        button.setAutoRepeat(auto_repeat)

        return button

    def _generate_spinbox(self, lower: float = -1e8, upper: float = 1e8,
                          decimals: int = 2, step: float = 1.0) -> QAbstractSpinBox:
        spinbox = QDoubleSpinBox(self)
        spinbox.setMinimum(lower)
        spinbox.setMaximum(upper)
        spinbox.setDecimals(decimals)
        spinbox.setSingleStep(step)
        spinbox.setMinimumWidth(10)

        return spinbox

    def _connect_internal_signals(self) -> None:
        self.button_visibility.toggled.connect(self.signal_visibility_requested.emit)
        self.button_grid_color.clicked.connect(self.signal_grid_color_requested.emit)
        self.button_text_color.clicked.connect(self.signal_text_color_requested.emit)

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

        self.button_grid_color.setStyleSheet(self._get_button_stylesheet(viewer.grid.grid_color))
        self.button_text_color.setStyleSheet(self._get_button_stylesheet(viewer.grid.text_color))

        # Connect signals
        def handle_grid_visibility(status: bool) -> None:
            viewer.grid.is_visible = status
            self.button_visibility.setText('Visible' if status else 'Hidden')

        def handle_color(title: str, original_color: iter) -> iter:
            dialog = QColorDialog()
            dialog.setOption(QColorDialog.DontUseNativeDialog)

            dialog.setWindowTitle(title)
            dialog.setCurrentColor(QColor.fromRgbF(*original_color))

            status = dialog.exec()

            if status:
                return dialog.currentColor().getRgbF()[:3]

            return original_color

        def handle_grid_color() -> None:
            color = handle_color('Grid Color', viewer.grid.grid_color)
            viewer.grid.grid_color = color
            self.button_grid_color.setStyleSheet(self._get_button_stylesheet(color))

            viewer.makeCurrent()
            viewer.grid.setup_attributes()
            viewer.recreate()

        def handle_text_color() -> None:
            color = handle_color('Text Color', viewer.grid.text_color)
            viewer.grid.text_color = color
            self.button_text_color.setStyleSheet(self._get_button_stylesheet(color))

            viewer.makeCurrent()
            viewer.grid.setup_attributes()
            viewer.recreate()

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

        self.signal_visibility_requested.connect(handle_grid_visibility)
        self.signal_grid_color_requested.connect(handle_grid_color)
        self.signal_text_color_requested.connect(handle_text_color)

        self.signal_separation_altered.connect(handle_grid_separation)
        self.signal_origin_altered.connect(handle_grid_origin)
        self.signal_length_altered.connect(handle_grid_length)

    def get_visibility(self) -> bool:
        return self.button_visibility.isChecked()

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
        self.button_visibility.setChecked(value)
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
