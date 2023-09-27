#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QColor

from .treewidgetitem import TreeWidgetItem
from .customwidgets.colordialog import ColorDialog


class MeshTreeWidgetItem(TreeWidgetItem):
    def __init__(self, parent=None, drawable=None):
        super().__init__(parent, drawable)

    def toggle_highlighting(self) -> None:
        self.drawable.toggle_highlighting()

    def toggle_wireframe(self) -> None:
        self.drawable.toggle_wireframe()

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
