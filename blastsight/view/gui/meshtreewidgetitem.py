#!/usr/bin/env python

#  Copyright (c) 2019-2024 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QColor
from qtpy.QtWidgets import QMenu

from .actioncollection import ActionCollection
from .customwidgets.colordialog import ColorDialog
from .treewidgetitem import TreeWidgetItem


class MeshTreeWidgetItem(TreeWidgetItem):
    def __init__(self, parent=None, drawable=None):
        super().__init__(parent, drawable)

    def toggle_highlighting(self) -> None:
        self.drawable.toggle_highlighting()

    def toggle_wireframe(self) -> None:
        self.drawable.toggle_wireframe()

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
    Context menu
    """
    def generate_context_menu(self, viewer, tree) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(tree)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        # Dynamic checkbox in actions
        actions.action_highlight.setChecked(self.drawable.is_highlighted)
        actions.action_wireframe.setChecked(self.drawable.is_wireframed)

        menu.addAction(actions.action_highlight)
        menu.addAction(actions.action_wireframe)

        menu.addAction(actions.action_setup_colors)
        menu.addSeparator()

        menu.addAction(actions.action_export_element)
        menu.addAction(actions.action_delete)

        self.connect_actions(actions, viewer, tree)
        return menu

    """
    Actions
    """
    def connect_actions(self, actions: list, viewer, tree) -> None:
        super().connect_actions(actions, viewer, tree)

        actions.action_highlight.triggered.connect(self.toggle_highlighting)
        actions.action_wireframe.triggered.connect(self.toggle_wireframe)
