#!/usr/bin/env python

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QAction
from qtpy.QtWidgets import QMenu
from qtpy.QtWidgets import QTreeWidget
from ..Drawables.meshgl import MeshGL
from ..Drawables.blockmodelgl import BlockModelGL
from ..Drawables.pointgl import PointGL


class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.itemClicked.connect(self.single_click)
        self.itemDoubleClicked.connect(self.double_click)
        self.customContextMenuRequested.connect(self.context_menu)

        # # Qt documentation states that user types should begin at this value.
        # self.type_mesh = QTreeWidgetItem.UserType
        # self.type_block_model = QTreeWidgetItem.UserType + 1

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
        action_wireframe = QAction('&Toggle wireframe', self)
        action_available_values = QAction('&Available values', self)

        # Icons
        icon = QIcon.fromTheme('show-hidden')
        action_show.setIcon(icon)
        icon = QIcon.fromTheme('object-hidden')
        action_hide.setIcon(icon)
        icon = QIcon.fromTheme('stock_close')
        action_delete.setIcon(icon)
        icon = QIcon.fromTheme('draw-triangle')
        action_wireframe.setIcon(icon)
        icon = QIcon.fromTheme('auto-type')
        action_available_values.setIcon(icon)
        icon = QIcon.fromTheme('camera')
        action_center_camera.setIcon(icon)

        # Action commands
        action_show.triggered.connect(item.show)
        action_hide.triggered.connect(item.hide)
        action_delete.triggered.connect(item.delete)
        action_wireframe.triggered.connect(item.toggle_wireframe)
        action_center_camera.triggered.connect(item.center_camera)
        action_available_values.triggered.connect(item.available_value_names)

        # Add actions depending on item type
        menu.addAction(action_show)
        menu.addAction(action_hide)
        menu.addAction(action_center_camera)

        if item.type == MeshGL:
            menu.addAction(action_wireframe)
        elif item.type == BlockModelGL or item.type == PointGL:
            menu.addAction(action_available_values)

        menu.addSeparator()
        menu.addAction(action_delete)

        menu.exec_(global_pos)

    def single_click(self, item, col):
        print('single_click')

    def double_click(self, item):
        item.toggle_visibility()

    def select_item(self, row, col):
        self.setCurrentItem(self.topLevelItem(max(min(row, self.topLevelItemCount() - 1), 0)), col)

    def keyPressEvent(self, event):
        if self.topLevelItemCount() == 0:
            return

        last_pos = self.indexOfTopLevelItem(self.currentItem())

        if event.key() == Qt.Key_Delete:
            self.currentItem().delete()
            self.select_item(last_pos, 0)
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.currentItem().center_camera()
        elif event.key() == Qt.Key_H:
            self.currentItem().hide()
        elif event.key() == Qt.Key_S:
            self.currentItem().show()
        elif event.key() == Qt.Key_T:
            self.currentItem().toggle_visibility()
        elif event.key() == Qt.Key_Up:
            self.select_item(last_pos - 1, 0)
        elif event.key() == Qt.Key_Down:
            self.select_item(last_pos + 1, 0)
        elif event.key() == Qt.Key_Home:
            self.select_item(0, 0)
        elif event.key() == Qt.Key_End:
            self.select_item(self.topLevelItemCount() - 1, 0)
