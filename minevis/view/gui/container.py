#!/usr/bin/env python

from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

from .toolbar import ToolBar
from .integrableviewer import IntegrableViewer
from .cameradialog import CameraDialog
from .treewidget import TreeWidget


class Container(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        self.mainToolBar = ToolBar(self)
        self.openglwidget = IntegrableViewer(self)
        self.treeWidget = TreeWidget()
        self.treeWidget.setWindowTitle('Drawables')

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.openglwidget)
        self.verticalLayout.addWidget(self.mainToolBar)

        self.setWindowTitle('MineVis (Container)')
        self.setMinimumSize(600, 500)

        self.toolbar.insertAction(self.toolbar.action_plan_view, self.toolbar.action_camera_properties)
        self.toolbar.addAction(self.toolbar.action_quit)

        self.toolbar.connect_tree(self.treeWidget)
        self.toolbar.connect_viewer(self.viewer)

        self.connect_actions()

    @property
    def viewer(self):
        return self.openglwidget

    @property
    def toolbar(self):
        return self.mainToolBar

    def connect_actions(self):
        self.toolbar.action_camera_properties.triggered.connect(self.camera_properties_dialog)
        self.toolbar.action_quit.triggered.connect(self.close)
        self.viewer.file_modified_signal.connect(self.fill_tree_widget)

    def camera_properties_dialog(self):
        dialog = CameraDialog(self.viewer)
        dialog.show()

    def fill_tree_widget(self) -> None:
        self.treeWidget.fill_from_viewer(self.viewer)

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
