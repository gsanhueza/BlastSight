#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QFont
from qtpy.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
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

    def toggle_highlighting(self) -> None:
        self.drawable.toggle_highlighting()

    def toggle_wireframe(self) -> None:
        self.drawable.toggle_wireframe()

    def toggle_visibility(self) -> None:
        self.drawable.toggle_visibility()
        self.set_visible(self.drawable.is_visible)
