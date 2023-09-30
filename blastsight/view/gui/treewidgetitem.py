#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Signal
from qtpy.QtGui import QColor
from qtpy.QtGui import QFont
from qtpy.QtWidgets import QTreeWidgetItem

from .customwidgets.colordialog import ColorDialog


class TreeWidgetItem(QTreeWidgetItem):
    signal_export_element = Signal()

    def __init__(self, parent=None, drawable=None):
        super().__init__(parent)
        self.drawable = drawable

        self.setText(0, f'{drawable.name}.{drawable.extension} (id: {drawable.id})')
        self.set_visible(drawable.is_visible)

    @property
    def id(self) -> int:
        return self.drawable.id

    def set_visible(self, is_visible: bool) -> None:
        font = QFont()
        font.setBold(is_visible)
        font.setItalic(not is_visible)
        self.setFont(0, font)

    def show(self) -> None:
        self.drawable.show()
        self.set_visible(self.drawable.is_visible)

    def hide(self) -> None:
        self.drawable.hide()
        self.set_visible(self.drawable.is_visible)

    def toggle_visibility(self) -> None:
        self.drawable.toggle_visibility()
        self.set_visible(self.drawable.is_visible)

    """
    Element properties handling
    """
    def update_color(self, viewer, color: iter) -> None:
        viewer.get_drawable(self.id).rgba = color
        viewer.update_drawable(self.id)

    def handle_color(self, viewer) -> None:
        element = viewer.get_drawable(self.id)

        dialog = ColorDialog()
        dialog.setCurrentColor(QColor.fromRgbF(*element.rgba))
        dialog.accepted.connect(lambda: self.update_color(viewer, dialog.currentColor().getRgbF()))
        dialog.show()

    """
    Actions
    """
    def connect_actions(self, actions: list) -> None:
        actions.action_export_element.triggered.connect(lambda: self.signal_export_element.emit(self.id))
