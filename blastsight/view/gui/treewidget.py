#!/usr/bin/env python

#  Copyright (c) 2019-2024 Gabriel Sanhueza.
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
from .meshtreewidgetitem import MeshTreeWidgetItem
from .blocktreewidgetitem import BlockTreeWidgetItem

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

    def auto_refill(self) -> None:
        self.clear()

        for drawable in self.available_drawables():
            item_widget = self.generate_item(drawable)
            self.addTopLevelItem(item_widget)

    def available_drawables(self) -> list:
        return self.viewer.get_all_drawables()

    def generate_item(self, drawable) -> TreeWidgetItem:
        if isinstance(drawable, MeshGL):
            return MeshTreeWidgetItem(self, drawable)
        elif isinstance(drawable, BlockGL) or isinstance(drawable, PointGL):
            return BlockTreeWidgetItem(self, drawable)
        else:
            return TreeWidgetItem(self, drawable)

    def context_menu(self, event) -> None:
        # Pop-up the context menu on current position, if an item is there
        item = self.itemAt(event)

        if item:
            self.show_context_menu(item, self.viewport().mapToGlobal(event))

    def generate_multiple_menu(self, action_squeezer: callable) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(self)

        actions.action_show.triggered.connect(self.show_items)
        actions.action_hide.triggered.connect(self.hide_items)
        actions.action_delete.triggered.connect(self.delete_items)
        actions.action_focus_camera.triggered.connect(self.center_camera)
        actions.action_setup_multiple.triggered.connect(
            lambda: self.handle_multiple(self.selectedItems()))

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addSeparator()

        # Call the method that squeezes more actions before the export/delete ones
        action_squeezer(menu, actions)

        menu.addAction(actions.action_delete)

        return menu

    def show_context_menu(self, item, global_pos) -> None:
        def action_squeezer(menu: QMenu, actions: ActionCollection) -> None:
            menu.addAction(actions.action_setup_multiple)
            menu.addSeparator()

        # If multiple elements are selected, we'll only show a basic menu
        if len(self.selectedItems()) > 1:
            if all(map(lambda it: type(it.drawable) in [MeshGL, LineGL, TubeGL], self.selectedItems())):
                ctx_menu = self.generate_multiple_menu(action_squeezer)
            else:
                ctx_menu = self.generate_multiple_menu(lambda *_: None)
        else:
            # Else, we'll show the item's menu
            ctx_menu = item.generate_context_menu(self.viewer, self)

        ctx_menu.exec_(global_pos)

    def center_camera(self) -> None:
        row = min(map(self.indexOfTopLevelItem, self.selectedItems()), default=0)
        item = self.topLevelItem(row)
        item.center_camera(self.viewer)

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
