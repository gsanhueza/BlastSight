#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QFont
from qtpy.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, viewer=None, _id=None):
        super().__init__(parent)
        self.viewer = viewer
        self.id = _id
        self.setText(0, f'{self.name}.{self.ext} (id: {self.id})')
        self.set_visible(self.drawable.is_visible)

    @property
    def name(self) -> str:
        return self.drawable.element.name

    @property
    def ext(self) -> str:
        return self.drawable.element.extension

    @property
    def type(self) -> type:
        return type(self.drawable)

    @property
    def drawable(self):
        return self.viewer.get_drawable(self.id)

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

    def delete(self, no_signal=False) -> None:
        self.viewer.blockSignals(no_signal)

        self.viewer.delete(self.drawable.id)

        self.viewer.blockSignals(False)
        self.viewer = None

    def toggle_highlighting(self) -> None:
        self.drawable.toggle_highlighting()

    def toggle_wireframe(self) -> None:
        self.drawable.toggle_wireframe()

    def toggle_visibility(self) -> None:
        self.drawable.toggle_visibility()
        self.set_visible(self.drawable.is_visible)

    def center_camera(self) -> None:
        self.viewer.camera_at(self.drawable.id)
