#!/usr/bin/env python

#  Copyright (c) 2019-2024 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QColor
from qtpy.QtGui import QFont

from qtpy.QtWidgets import QMenu
from qtpy.QtWidgets import QTreeWidgetItem

from .actioncollection import ActionCollection
from .customwidgets.colordialog import ColorDialog


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

    def toggle_visibility(self) -> None:
        self.drawable.toggle_visibility()
        self.set_visible(self.drawable.is_visible)

    def center_camera(self, viewer) -> None:
        self.show()
        viewer.show_drawable(self.id)
        viewer.camera_at(self.id)

    def delete(self, viewer) -> None:
        viewer.delete(self.id)

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
    def connect_actions(self, actions: list, viewer, tree) -> None:
        actions.action_show.triggered.connect(self.show)
        actions.action_hide.triggered.connect(self.hide)
        actions.action_focus_camera.triggered.connect(lambda: self.center_camera(viewer))
        actions.action_setup_colors.triggered.connect(lambda: self.handle_color(viewer))

        actions.action_export_element.triggered.connect(lambda: tree.signal_export_element.emit(self.id))
        actions.action_delete.triggered.connect(lambda: self.delete(viewer))

    """
    Context menu
    """
    def generate_context_menu(self, viewer, tree) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(tree)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        menu.addAction(actions.action_setup_colors)
        menu.addSeparator()

        menu.addAction(actions.action_export_element)
        menu.addAction(actions.action_delete)

        self.connect_actions(actions, viewer, tree)
        return menu
