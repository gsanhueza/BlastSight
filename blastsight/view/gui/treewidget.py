#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QAbstractItemView
from qtpy.QtWidgets import QMenu
from qtpy.QtWidgets import QTreeWidget
from qtpy.QtWidgets import QTreeWidgetItemIterator

from .treewidgetitem import TreeWidgetItem
from .actioncollection import ActionCollection

from ..drawables.meshgl import MeshGL
from ..drawables.blockgl import BlockGL
from ..drawables.pointgl import PointGL
from ..drawables.linegl import LineGL


class TreeWidget(QTreeWidget):
    signal_headers_triggered = Signal(int)
    signal_colors_triggered = Signal(int)
    signal_export_mesh = Signal(int)
    signal_export_blocks = Signal(int)
    signal_export_points = Signal(int)
    signal_export_lines = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.itemDoubleClicked.connect(self.center_camera)
        self.customContextMenuRequested.connect(self.context_menu)

        self.setWindowTitle('Element list')
        self.headerItem().setText(0, 'Elements')

    def fill_from_viewer(self, viewer) -> None:
        self.clear()
        # Copy the OrderedDict to avoid exception
        # RuntimeError: OrderedDict mutated during iteration
        drawables = viewer.drawable_collection.copy().values()

        for drawable in drawables:
            item = TreeWidgetItem(self, viewer, drawable.id)
            self.addTopLevelItem(item)

    def context_menu(self, event) -> None:
        # Pop-up the context menu on current position, if an item is there
        item = self.itemAt(event)

        if item:
            self.show_context_menu(item, self.viewport().mapToGlobal(event))

    def show_context_menu(self, item, global_pos):
        menu = QMenu()
        actions = ActionCollection(self)

        # Action commands
        actions.action_show.triggered.connect(self.show_items)
        actions.action_hide.triggered.connect(self.hide_items)
        actions.action_delete.triggered.connect(self.delete_items)

        actions.action_highlight.triggered.connect(item.toggle_highlighting)
        actions.action_wireframe.triggered.connect(item.toggle_wireframe)

        actions.action_properties.triggered.connect(lambda: self.signal_headers_triggered.emit(item.id))
        actions.action_colors.triggered.connect(lambda: self.signal_colors_triggered.emit(item.id))
        actions.action_center_camera.triggered.connect(item.center_camera)

        actions.action_export_mesh.triggered.connect(lambda: self.signal_export_mesh.emit(item.id))
        actions.action_export_blocks.triggered.connect(lambda: self.signal_export_blocks.emit(item.id))
        actions.action_export_points.triggered.connect(lambda: self.signal_export_points.emit(item.id))
        actions.action_export_lines.triggered.connect(lambda: self.signal_export_lines.emit(item.id))

        # If multiple elements are selected, we'll only show a basic menu
        if len(self.selectedItems()) > 1:
            menu.addAction(actions.action_show)
            menu.addAction(actions.action_hide)
            menu.addSeparator()
            menu.addAction(actions.action_delete)
            menu.exec_(global_pos)

            return

        # Add actions depending on item type
        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_center_camera)

        # WARNING: MeshGL.is_boostable == True means no highlight/wireframe support yet.
        if item.type is MeshGL:
            # Dynamic text fixing in actions
            text = f'{"Disable" if item.drawable.is_highlighted else "Enable"} h&ighlighting'
            actions.action_highlight.setText(text)

            text = f'{"Disable" if item.drawable.is_wireframed else "Enable"} &wireframe'
            actions.action_wireframe.setText(text)

            menu.addAction(actions.action_highlight)
            menu.addAction(actions.action_wireframe)
            menu.addAction(actions.action_colors)
            menu.addSeparator()
            menu.addAction(actions.action_export_mesh)
        elif item.type is LineGL:
            menu.addAction(actions.action_colors)
            menu.addSeparator()
            menu.addAction(actions.action_export_lines)
        elif item.type is BlockGL:
            menu.addAction(actions.action_properties)
            menu.addSeparator()
            menu.addAction(actions.action_export_blocks)
        elif item.type is PointGL:
            menu.addAction(actions.action_properties)
            menu.addSeparator()
            menu.addAction(actions.action_export_points)

        menu.addAction(actions.action_delete)

        menu.exec_(global_pos)

    def center_camera(self):
        row = min([self.indexOfTopLevelItem(x) for x in self.selectedItems()], default=0)
        self.topLevelItem(row).show()
        self.topLevelItem(row).center_camera()

    def select_item(self, row):
        row = max(min(row, self.topLevelItemCount() - 1), 0)
        item = self.topLevelItem(row)
        item.setSelected(True)
        self.scrollToItem(item, QAbstractItemView.EnsureVisible)

    def select_by_id_list(self, id_list):
        it = QTreeWidgetItemIterator(self)

        first_item = False
        while it.value():
            item = it.value()
            if item.id in id_list:
                if not first_item:
                    self.setCurrentItem(item)
                    first_item = True

                self.select_item(self.indexOfTopLevelItem(item))
            it += 1

    def show_items(self):
        for item in self.selectedItems():
            item.show()

    def hide_items(self):
        for item in self.selectedItems():
            item.hide()

    def toggle_items_visibility(self):
        for item in self.selectedItems():
            item.toggle_visibility()

    def delete_items(self):
        closest_row = min([self.indexOfTopLevelItem(x) for x in self.selectedItems()], default=0)

        # We'll trick the viewer so it doesn't emit file_modified_signal until last item
        # has been deleted, so we're not forced to auto-fill for each deleted item.
        selected = self.selectedItems()
        for item in selected[:-1]:
            item.delete(no_signal=True)

        if len(selected) > 0:
            selected[-1].delete()

        self.setCurrentItem(self.topLevelItem(max(closest_row - 1, 0)))

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if self.topLevelItemCount() == 0:
            return

        shortcut_commands_dict = {
            Qt.Key_Space: self.toggle_items_visibility,
            Qt.Key_Delete: self.delete_items,
            Qt.Key_Enter: self.center_camera,
            Qt.Key_Return: self.center_camera,
        }

        # Execute command based on event.key()
        shortcut_commands_dict.get(event.key(), lambda: None)()
