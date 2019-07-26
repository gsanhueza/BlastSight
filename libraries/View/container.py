#!/usr/bin/env python

from qtpy.QtWidgets import QWidget, QVBoxLayout
from .GUI.toolbar import ToolBar
from .GUI.integrableviewer import IntegrableViewer
from .GUI.camerapositiondialog import CameraPositionDialog


class Container(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        self.mainToolBar = ToolBar(self)
        self.openglwidget = IntegrableViewer(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.mainToolBar)
        self.verticalLayout.addWidget(self.openglwidget)

        self.setWindowTitle('MineVis (Container)')
        self.setMinimumSize(400, 300)

        self.connect_actions()

    @property
    def viewer(self):
        return self.openglwidget

    def connect_actions(self):
        self.mainToolBar.action_camera_position.triggered.connect(self.dialog_camera_position)
        self.mainToolBar.action_plan_view.triggered.connect(self.viewer.plan_view)
        self.mainToolBar.action_north_view.triggered.connect(self.viewer.north_view)
        self.mainToolBar.action_east_view.triggered.connect(self.viewer.east_view)
        self.mainToolBar.action_take_screenshot.triggered.connect(self.viewer.take_screenshot)
        self.mainToolBar.action_quit.triggered.connect(self.close)

    def dialog_camera_position(self):
        dialog = CameraPositionDialog(self)
        dialog.show()
