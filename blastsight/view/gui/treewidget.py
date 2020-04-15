#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import json

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QAbstractItemView
from qtpy.QtWidgets import QMenu
from qtpy.QtWidgets import QTreeWidget
from qtpy.QtWidgets import QTreeWidgetItemIterator

from .treewidgetitem import TreeWidgetItem
from .actioncollection import ActionCollection

from .colordialog import ColorDialog
from .propertiesdialog import PropertiesDialog

from ..drawables.meshgl import MeshGL
from ..drawables.blockgl import BlockGL
from ..drawables.pointgl import PointGL
from ..drawables.linegl import LineGL
from ..drawables.tubegl import TubeGL


class TreeWidget(QTreeWidget):
    signal_headers_triggered = Signal(int)
    signal_colors_triggered = Signal(int)
    signal_export_mesh = Signal(int)
    signal_export_blocks = Signal(int)
    signal_export_points = Signal(int)
    signal_export_lines = Signal(int)
    signal_export_tubes = Signal(int)

    def __init__(self, parent=None, viewer=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.itemDoubleClicked.connect(self.center_camera)
        self.customContextMenuRequested.connect(self.context_menu)

        self.setWindowTitle('Element list')
        self.headerItem().setText(0, 'Elements')

        self.viewer = viewer
        self.is_export_enabled = False

    def connect_viewer(self, viewer) -> None:
        self.viewer = viewer
        self.viewer.signal_file_modified.connect(self.auto_refill)
        self.viewer.signal_mesh_clicked.connect(self.handle_mesh_clicked)
        self.signal_colors_triggered.connect(self.handle_color)
        self.signal_headers_triggered.connect(self.handle_properties)

    def handle_mesh_clicked(self, attributes: list) -> None:
        self.select_by_id_list([attr.get('id', -1) for attr in attributes])

    def handle_color(self, _id: int) -> None:
        element = self.viewer.get_drawable(_id)
        dialog = ColorDialog(self.viewer, element)
        dialog.accepted.connect(lambda: self.update_color(dialog, element))
        dialog.show()

    def update_color(self, dialog, element) -> None:
        element.rgba = [x / 255 for x in dialog.currentColor().getRgb()]
        self.viewer.update_drawable(element.id)

    def handle_properties(self, _id: int) -> None:
        element = self.viewer.get_drawable(_id)
        dialog = PropertiesDialog(self.viewer, element)
        dialog.accepted.connect(lambda: self.update_properties(dialog, element))
        dialog.show()

    def update_properties(self, dialog, element) -> None:
        # Parse values in QTableWidget
        for i in range(dialog.tableWidget_properties.rowCount()):
            k = dialog.tableWidget_properties.verticalHeaderItem(i).text()
            v = dialog.tableWidget_properties.item(i, 0).text()
            try:
                setattr(element, k, float(v))
            except ValueError:  # Element might be a list or string
                try:  # Element is a list
                    setattr(element, k, json.loads(v))
                except json.decoder.JSONDecodeError:  # Element is a string
                    setattr(element, k, v)
            except KeyError:  # Element clearly is not a property
                print(f'{k} property does not exist.')

        # Update headers
        altered = dialog.has_altered_coordinates(element)
        element.headers = dialog.current_headers

        # Recreate instance with the "new" data
        self.viewer.update_drawable(element.id)

        # If coordinates were altered and auto-fit is enabled, call fit_to_screen()
        if altered and self.viewer.get_autofit_status():
            self.viewer.fit_to_screen()

    def enable_exportability(self, value: bool) -> None:
        self.is_export_enabled = value

    def auto_refill(self) -> None:
        self.clear()

        for drawable in self.viewer.get_all_drawables():
            self.addTopLevelItem(TreeWidgetItem(self, drawable))

    def context_menu(self, event) -> None:
        # Pop-up the context menu on current position, if an item is there
        item = self.itemAt(event)

        if item:
            self.show_context_menu(item, self.viewport().mapToGlobal(event))

    def connect_actions(self, actions: ActionCollection, item: TreeWidgetItem) -> None:
        self._connect_standalone_actions(actions)
        self._connect_item_actions(actions, item)

    def _connect_standalone_actions(self, actions: ActionCollection) -> None:
        actions.action_show.triggered.connect(self.show_items)
        actions.action_hide.triggered.connect(self.hide_items)
        actions.action_delete.triggered.connect(self.delete_items)
        actions.action_focus_camera.triggered.connect(self.center_camera)

    def _connect_item_actions(self, actions: ActionCollection, item: TreeWidgetItem) -> None:
        actions.action_highlight.triggered.connect(item.toggle_highlighting)
        actions.action_wireframe.triggered.connect(item.toggle_wireframe)

        actions.action_properties.triggered.connect(lambda: self.signal_headers_triggered.emit(item.id))
        actions.action_setup_colors.triggered.connect(lambda: self.signal_colors_triggered.emit(item.id))

        actions.action_export_mesh.triggered.connect(lambda: self.signal_export_mesh.emit(item.id))
        actions.action_export_blocks.triggered.connect(lambda: self.signal_export_blocks.emit(item.id))
        actions.action_export_points.triggered.connect(lambda: self.signal_export_points.emit(item.id))
        actions.action_export_lines.triggered.connect(lambda: self.signal_export_lines.emit(item.id))
        actions.action_export_tubes.triggered.connect(lambda: self.signal_export_tubes.emit(item.id))

    def generate_multiple_menu(self) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)
        self._connect_standalone(actions)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addSeparator()
        menu.addAction(actions.action_delete)

        return menu

    def generate_mesh_menu(self, item: TreeWidgetItem) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)
        self.connect_actions(actions, item)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        # Dynamic checkbox in actions
        actions.action_highlight.setChecked(item.drawable.is_highlighted)
        actions.action_wireframe.setChecked(item.drawable.is_wireframed)

        menu.addAction(actions.action_highlight)
        menu.addAction(actions.action_wireframe)

        menu.addAction(actions.action_setup_colors)
        menu.addSeparator()

        if self.is_export_enabled:
            menu.addAction(actions.action_export_mesh)
        menu.addAction(actions.action_delete)

        return menu

    def generate_blocks_menu(self, item: TreeWidgetItem) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)
        self.connect_actions(actions, item)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        menu.addAction(actions.action_properties)
        menu.addSeparator()

        if self.is_export_enabled:
            menu.addAction(actions.action_export_blocks)
        menu.addAction(actions.action_delete)

        return menu

    def generate_points_menu(self, item: TreeWidgetItem) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)
        self.connect_actions(actions, item)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        menu.addAction(actions.action_properties)
        menu.addSeparator()

        if self.is_export_enabled:
            menu.addAction(actions.action_export_points)
        menu.addAction(actions.action_delete)

        return menu

    def generate_lines_menu(self, item: TreeWidgetItem) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)
        self.connect_actions(actions, item)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        menu.addAction(actions.action_setup_colors)
        menu.addSeparator()

        if self.is_export_enabled:
            menu.addAction(actions.action_export_lines)
        menu.addAction(actions.action_delete)

        return menu

    def generate_tubes_menu(self, item: TreeWidgetItem) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)
        self.connect_actions(actions, item)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        menu.addAction(actions.action_setup_colors)
        menu.addSeparator()

        if self.is_export_enabled:
            menu.addAction(actions.action_export_tubes)
        menu.addAction(actions.action_delete)

        return menu

    def show_context_menu(self, item, global_pos) -> None:
        menus_dict = {
            MeshGL: lambda: self.generate_mesh_menu(item),
            BlockGL: lambda: self.generate_blocks_menu(item),
            PointGL: lambda: self.generate_points_menu(item),
            LineGL: lambda: self.generate_lines_menu(item),
            TubeGL: lambda: self.generate_tubes_menu(item),
        }

        # If multiple elements are selected, we'll only show a basic menu
        if len(self.selectedItems()) > 1:
            menu = self.generate_multiple_menu()
        else:
            menu = menus_dict.get(type(item.drawable))()

        menu.exec_(global_pos)

    def center_camera(self) -> None:
        row = min([self.indexOfTopLevelItem(x) for x in self.selectedItems()], default=0)
        drawable = self.topLevelItem(row).drawable
        self.viewer.show_drawable(drawable.id)
        self.viewer.camera_at(drawable.id)

    def select_item(self, row: int) -> None:
        row = max(min(row, self.topLevelItemCount() - 1), 0)
        item = self.topLevelItem(row)
        if item:
            item.setSelected(True)
            self.scrollToItem(item, QAbstractItemView.EnsureVisible)

    def select_by_id_list(self, id_list: list) -> None:
        self.clearSelection()
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

    def show_items(self) -> None:
        for item in self.selectedItems():
            item.show()

    def hide_items(self) -> None:
        for item in self.selectedItems():
            item.hide()

    def toggle_items_visibility(self) -> None:
        for item in self.selectedItems():
            item.toggle_visibility()

    def delete_items(self) -> None:
        closest_row = min([self.indexOfTopLevelItem(x) for x in self.selectedItems()], default=0)

        # We'll trick the viewer so it doesn't emit file_modified_signal until last item
        # has been deleted, so we're not forced to auto-fill for each deleted item.
        self.viewer.blockSignals(True)

        for _id in [item.drawable.id for item in self.selectedItems()]:
            self.viewer.delete(_id)

        self.viewer.blockSignals(False)
        self.viewer.signal_file_modified.emit()

        self.setCurrentItem(self.topLevelItem(max(closest_row - 1, 0)))

    def keyPressEvent(self, event: QKeyEvent) -> None:
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
