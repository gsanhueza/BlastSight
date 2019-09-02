#!/usr/bin/env python

from qtpy.QtCore import Qt
from qtpy.QtCore import Signal
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QAction
from qtpy.QtWidgets import QMenu
from qtpy.QtWidgets import QTreeWidget
from .treewidgetitem import TreeWidgetItem
from ..drawables.meshgl import MeshGL
from ..drawables.blockgl import BlockGL
from ..drawables.pointgl import PointGL


class TreeWidget(QTreeWidget):
    headers_triggered_signal = Signal(int)
    colors_triggered_signal = Signal(int)
    export_mesh_signal = Signal(int)
    export_blocks_signal = Signal(int)
    export_points_signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.itemClicked.connect(self.single_click)
        self.itemDoubleClicked.connect(self.double_click)
        self.customContextMenuRequested.connect(self.context_menu)

    def fill_from_viewer(self, viewer) -> None:
        self.clear()

        for drawable in viewer.drawable_collection.values():
            item = TreeWidgetItem(self, viewer, drawable.id)
            self.addTopLevelItem(item)
        self.select_item(self.topLevelItemCount(), 0)

    def context_menu(self, event) -> None:
        """
        Creates a context menu when the user does a right click.

        :param event: Qt Event.
        :return: None
        """
        # Pop-up the context menu on current position, if an item is there
        item = self.itemAt(event)

        if item:
            self.show_context_menu(item, self.viewport().mapToGlobal(event))

    def show_context_menu(self, item, global_pos):
        menu = QMenu()

        # Actions
        action_show = QAction('&Show', self)
        action_hide = QAction('&Hide', self)
        action_delete = QAction('&Delete', self)
        action_center_camera = QAction('&Center camera', self)
        action_highlight = QAction('T&oggle highlighting', self)
        action_wireframe = QAction('&Toggle wireframe', self)
        action_headers = QAction('H&eaders', self)
        action_colors = QAction('C&olors', self)
        action_export_mesh = QAction('&Export mesh', self)
        action_export_blocks = QAction('Export &blocks', self)
        action_export_points = QAction('Export &points', self)

        # Icons
        action_show.setIcon(QIcon.fromTheme('show-hidden'))
        action_hide.setIcon(QIcon.fromTheme('object-hidden'))
        action_delete.setIcon(QIcon.fromTheme('stock_close'))
        action_highlight.setIcon(QIcon.fromTheme('camera-ready'))
        action_wireframe.setIcon(QIcon.fromTheme('draw-triangle'))
        action_headers.setIcon(QIcon.fromTheme('auto-type'))
        action_center_camera.setIcon(QIcon.fromTheme('camera'))
        action_colors.setIcon(QIcon.fromTheme('colormanagement'))
        action_export_mesh.setIcon(QIcon.fromTheme('document-export'))
        action_export_blocks.setIcon(QIcon.fromTheme('document-export'))
        action_export_points.setIcon(QIcon.fromTheme('document-export'))

        # Action commands
        action_show.triggered.connect(item.show)
        action_hide.triggered.connect(item.hide)
        action_delete.triggered.connect(item.delete)
        action_highlight.triggered.connect(item.toggle_highlighting)
        action_wireframe.triggered.connect(item.toggle_wireframe)
        action_center_camera.triggered.connect(item.center_camera)

        action_headers.triggered.connect(lambda: self.headers_triggered_signal.emit(item.drawable.id))
        action_colors.triggered.connect(lambda: self.colors_triggered_signal.emit(item.drawable.id))

        action_export_mesh.triggered.connect(lambda: self.export_mesh_signal.emit(item.drawable.id))
        action_export_blocks.triggered.connect(lambda: self.export_blocks_signal.emit(item.drawable.id))
        action_export_points.triggered.connect(lambda: self.export_points_signal.emit(item.drawable.id))

        # Add actions depending on item type
        menu.addAction(action_show)
        menu.addAction(action_hide)
        menu.addAction(action_center_camera)

        if item.type == MeshGL:
            menu.addAction(action_highlight)
            menu.addAction(action_wireframe)
            menu.addAction(action_colors)
            menu.addSeparator()
            menu.addAction(action_export_mesh)
        elif item.type == BlockGL:
            menu.addAction(action_headers)
            menu.addSeparator()
            menu.addAction(action_export_blocks)
        elif item.type == PointGL:
            menu.addAction(action_headers)
            menu.addSeparator()
            menu.addAction(action_export_points)

        menu.addAction(action_delete)

        menu.exec_(global_pos)

    def single_click(self, item, col):
        pass

    def double_click(self, item):
        item.show()
        item.center_camera()

    def select_item(self, row, col):
        self.setCurrentItem(self.topLevelItem(max(min(row, self.topLevelItemCount() - 1), 0)), col)

    def keyPressEvent(self, event):
        if self.topLevelItemCount() == 0:
            return

        last_pos = self.indexOfTopLevelItem(self.currentItem())

        def delete_current():
            self.currentItem().delete()
            self.select_item(last_pos, 0)

        shortcut_commands_dict = {
            Qt.Key_Delete: lambda: delete_current(),
            Qt.Key_Enter: lambda: self.currentItem().center_camera(),
            Qt.Key_Return: lambda: self.currentItem().center_camera(),
            Qt.Key_H: lambda: self.currentItem().hide(),
            Qt.Key_S: lambda: self.currentItem().show(),
            Qt.Key_T: lambda: self.currentItem().toggle_visibility(),
            Qt.Key_Up: lambda: self.select_item(last_pos - 1, 0),
            Qt.Key_Down: lambda: self.select_item(last_pos + 1, 0),
            Qt.Key_Home: lambda: self.select_item(0, 0),
            Qt.Key_End: lambda: self.select_item(self.topLevelItemCount() - 1, 0),
        }

        # Execute command based on event.key()
        shortcut_commands_dict.get(event.key(), lambda: None)()
