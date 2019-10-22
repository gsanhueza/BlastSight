#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from datetime import datetime

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

from .toolbar import ToolBar
from .cameradialog import CameraDialog
from .treewidget import TreeWidget
from ..integrableviewer import IntegrableViewer


class Container(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        self.toolbar = ToolBar(self)
        self.actions = self.toolbar.action_collection
        self.viewer = IntegrableViewer(self)
        self.treeWidget = TreeWidget()
        self.treeWidget.setWindowTitle('Drawables')

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.viewer)
        self.verticalLayout.addWidget(self.toolbar)

        self.setWindowTitle('BlastSight (Container)')
        self.setMinimumSize(600, 500)

        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.insertAction(self.actions.action_plan_view, self.actions.action_camera_properties)
        self.toolbar.addAction(self.actions.action_quit)

        self.toolbar.connect_tree(self.treeWidget)
        self.toolbar.connect_viewer(self.viewer)

        self.connect_actions()

    def connect_actions(self):
        self.actions.action_take_screenshot.triggered.connect(self.dialog_screenshot)
        self.actions.action_camera_properties.triggered.connect(self.dialog_camera)
        self.actions.action_quit.triggered.connect(self.close)
        self.viewer.signal_file_modified.connect(self.fill_tree_widget)

    def dialog_camera(self):
        dialog = CameraDialog(self.viewer)
        dialog.show()

    def dialog_screenshot(self):
        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self,
            directory=f'BlastSight Screenshot ({datetime.now().strftime("%Y%m%d-%H%M%S")})',
            filter='PNG image (*.png);;')

        if path != '':
            self.viewer.take_screenshot(path)

    def fill_tree_widget(self) -> None:
        self.treeWidget.fill_from_viewer(self.viewer)

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
