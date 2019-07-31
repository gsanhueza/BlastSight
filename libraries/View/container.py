#!/usr/bin/env python

from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

from .GUI.toolbar import ToolBar
from .GUI.integrableviewer import IntegrableViewer
from .GUI.camerapropertiesdialog import CameraPropertiesDialog
from .GUI.treewidget import TreeWidget
from .GUI.treewidgetitem import TreeWidgetItem


class Container(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        self.mainToolBar = ToolBar(self)
        self.openglwidget = IntegrableViewer(self)
        self.treeWidget = TreeWidget()
        self.treeWidget.setWindowTitle('Drawables')

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.mainToolBar)
        self.verticalLayout.addWidget(self.openglwidget)

        self.setWindowTitle('MineVis (Container)')
        self.setMinimumSize(400, 300)

        self.toolbar.insertAction(self.toolbar.action_plan_view, self.toolbar.action_camera_position)
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
        self.toolbar.action_camera_position.triggered.connect(self.camera_properties_dialog)
        self.toolbar.action_quit.triggered.connect(self.close)
        self.viewer.file_modified_signal.connect(self.fill_tree_widget)

    def camera_properties_dialog(self):
        dialog = CameraPropertiesDialog(self)
        dialog.show()

    def fill_tree_widget(self) -> None:
        self.treeWidget.fill_from_viewer(self.viewer)

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
