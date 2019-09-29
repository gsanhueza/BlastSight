#!/usr/bin/env python

from qtpy.QtGui import QFont
from qtpy.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, viewer=None, _id=None):
        super().__init__(parent)
        self._viewer = viewer
        self._id = _id
        self.setText(0, f'{self.name}.{self.ext} (id: {self._id})')
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
    def viewer(self):
        return self._viewer

    @property
    def drawable(self):
        return self.viewer.get_drawable(self._id)

    def set_visible(self, is_visible):
        font = QFont()
        font.setBold(is_visible)
        font.setItalic(not is_visible)
        self.setFont(0, font)

    def show(self) -> None:
        self.drawable.show()
        self.set_visible(self.drawable.is_visible)
        self.viewer.update()

    def hide(self) -> None:
        self.drawable.hide()
        self.set_visible(self.drawable.is_visible)
        self.viewer.update()

    def delete(self) -> None:
        self.viewer.delete(self.drawable.id)
        self.viewer.update()
        self._viewer = None

    def toggle_highlighting(self) -> None:
        self.drawable.toggle_highlighting()
        self.viewer.update()

    def toggle_wireframe(self) -> None:
        self.drawable.toggle_wireframe()
        self.viewer.update()

    def toggle_visibility(self) -> None:
        self.drawable.toggle_visibility()
        self.set_visible(self.drawable.is_visible)
        self.viewer.update()

    def center_camera(self) -> None:
        self.viewer.camera_at(self.drawable.id)