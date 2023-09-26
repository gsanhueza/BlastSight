#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QAbstractItemView
from qtpy.QtWidgets import QMenu
from qtpy.QtWidgets import QTreeWidget
from qtpy.QtWidgets import QTreeWidgetItemIterator

from .customwidgets.colordialog import ColorDialog
from .actioncollection import ActionCollection
from .treewidgetitem import TreeWidgetItem

from ..drawables.meshgl import MeshGL
from ..drawables.blockgl import BlockGL
from ..drawables.pointgl import PointGL
from ..drawables.linegl import LineGL
from ..drawables.tubegl import TubeGL


class TreeWidget(QTreeWidget):
    signal_export_element = Signal(int)

    def __init__(self, viewer=None, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.itemDoubleClicked.connect(self.center_camera)
        self.customContextMenuRequested.connect(self.context_menu)

        self.setWindowTitle('Element list')
        self.headerItem().setText(0, 'Elements')

        self.is_export_enabled = False
        self.viewer = viewer

    def connect_viewer(self, viewer=None) -> None:
        if bool(viewer):
            self.viewer = viewer
        if not bool(self.viewer):
            return

        self.viewer.signal_file_modified.connect(self.auto_refill)
        self.viewer.signal_elements_detected.connect(self.handle_elements_detected)

    def handle_elements_detected(self, attributes: list) -> None:
        self.select_by_id_list(list(map(lambda attr: attr.get('id', -1), attributes)))

    def handle_multiple(self, item_list: list) -> None:
        def update_multiple(color: iter):
            for item in item_list:
                item.update_color(self.viewer, color)

        dialog = ColorDialog()
        dialog.accepted.connect(lambda *_: update_multiple(dialog.currentColor().getRgbF()))

        dialog.show()

    def enable_exportability(self, value: bool) -> None:
        self.is_export_enabled = value

    def auto_refill(self) -> None:
        self.clear()

        for drawable in self.available_drawables():
            self.addTopLevelItem(self.generate_item(drawable))

    def available_drawables(self) -> list:
        return self.viewer.get_all_drawables()

    def generate_item(self, drawable) -> TreeWidgetItem:
        return TreeWidgetItem(self, drawable)

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

        actions.action_setup_colors.triggered.connect(lambda: item.handle_color(self.viewer))
        actions.action_properties.triggered.connect(lambda: item.handle_properties(self.viewer))

        actions.action_export_element.triggered.connect(lambda: self.signal_export_element.emit(item.id))

    def generate_multiple_menu(self, action_squeezer: callable = lambda *_: None) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)

        self._connect_standalone_actions(actions)
        actions.action_setup_multiple.triggered.connect(
            lambda: self.handle_multiple(self.selectedItems()))

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addSeparator()

        # Call the method that squeezes more actions before the export/delete ones
        action_squeezer(menu, actions)

        menu.addAction(actions.action_delete)

        return menu

    def generate_single_menu(self, item: TreeWidgetItem, action_squeezer: callable) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)
        self.connect_actions(actions, item)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        # Call the method that squeezes more actions before the export/delete ones
        action_squeezer(menu, actions)

        if self.is_export_enabled:
            menu.addAction(actions.action_export_element)
        menu.addAction(actions.action_delete)

        return menu

    def generate_mesh_menu(self, item: TreeWidgetItem) -> QMenu:
        def action_squeezer(menu: QMenu, actions: ActionCollection) -> None:
            # Dynamic checkbox in actions
            actions.action_highlight.setChecked(item.drawable.is_highlighted)
            actions.action_wireframe.setChecked(item.drawable.is_wireframed)

            menu.addAction(actions.action_highlight)
            menu.addAction(actions.action_wireframe)

            menu.addAction(actions.action_setup_colors)
            menu.addSeparator()

        return self.generate_single_menu(item, action_squeezer)

    def generate_standard_menu(self, item: TreeWidgetItem) -> QMenu:
        def action_squeezer(menu: QMenu, actions: ActionCollection) -> None:
            menu.addAction(actions.action_setup_colors)
            menu.addSeparator()

        return self.generate_single_menu(item, action_squeezer)

    def generate_dataframe_menu(self, item: TreeWidgetItem) -> QMenu:
        def action_squeezer(menu: QMenu, actions: ActionCollection) -> None:
            menu.addAction(actions.action_properties)
            menu.addSeparator()

        return self.generate_single_menu(item, action_squeezer)

    def show_context_menu(self, item, global_pos) -> None:
        menus_dict = {
            MeshGL: lambda: self.generate_mesh_menu(item),
            BlockGL: lambda: self.generate_dataframe_menu(item),
            PointGL: lambda: self.generate_dataframe_menu(item),
            LineGL: lambda: self.generate_standard_menu(item),
            TubeGL: lambda: self.generate_standard_menu(item),
        }

        def action_squeezer(menu: QMenu, actions: ActionCollection) -> None:
            menu.addAction(actions.action_setup_multiple)
            menu.addSeparator()

        # If multiple elements are selected, we'll only show a basic menu
        if len(self.selectedItems()) > 1:
            if all(map(lambda it: type(it.drawable) in [MeshGL, LineGL, TubeGL], self.selectedItems())):
                ctx_menu = self.generate_multiple_menu(action_squeezer)
            else:
                ctx_menu = self.generate_multiple_menu()
        else:
            ctx_menu = menus_dict.get(type(item.drawable))()

        ctx_menu.exec_(global_pos)

    def center_camera(self) -> None:
        row = min(map(self.indexOfTopLevelItem, self.selectedItems()), default=0)
        item = self.topLevelItem(row)
        drawable = item.drawable

        item.set_visible(True)
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
        closest_row = min(map(self.indexOfTopLevelItem, self.selectedItems()), default=0)

        # We'll trick the viewer so it doesn't emit file_modified_signal until last item
        # has been deleted, so we're not forced to auto-fill for each deleted item.
        self.viewer.blockSignals(True)

        for _id in map(lambda item: item.id, self.selectedItems()):
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
