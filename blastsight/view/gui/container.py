#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

from .toolbar import ToolBar
from .treewidget import TreeWidget
from .iconcollection import IconCollection
from ..integrableviewer import IntegrableViewer


class Container(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        self.toolbar = ToolBar(self)
        self.actions = self.toolbar.action_collection
        self.viewer = IntegrableViewer(self)

        self.treeWidget = TreeWidget(viewer=self.viewer)
        self.treeWidget.setWindowTitle('Drawables')

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.viewer)
        self.verticalLayout.addWidget(self.toolbar)

        self.setWindowTitle('BlastSight (Container)')
        self.setWindowIcon(IconCollection.get('blastsight.png'))
        self.setMinimumSize(600, 500)

        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.insertAction(self.actions.action_plan_view, self.actions.action_camera_properties)
        self.toolbar.addAction(self.actions.action_quit)

        self.connect_actions()

    def connect_actions(self) -> None:
        self.toolbar.connect_tree(self.treeWidget)
        self.toolbar.connect_viewer(self.viewer)
        self.toolbar.connect_main_widget(self)
        self.viewer.signal_file_modified.connect(self.treeWidget.auto_refill)

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
