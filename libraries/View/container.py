#!/usr/bin/env python

from qtpy.QtWidgets import QWidget, QVBoxLayout
from .GUI.toolbar import ToolBar
from .GUI.integrableviewer import IntegrableViewer
from .GUI.camerapositiondialog import CameraPositionDialog
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
        self.mainToolBar.action_show_tree.triggered.connect(self.treeWidget.show)
        self.mainToolBar.action_quit.triggered.connect(self.close)
        self.viewer.file_dropped_signal.connect(self.fill_tree_widget)

    def dialog_camera_position(self):
        dialog = CameraPositionDialog(self)
        dialog.show()

    def fill_tree_widget(self) -> None:
        # Tree widget
        self.treeWidget.clear()

        for drawable in self.viewer.drawable_collection.values():
            if type(drawable.id) is int:
                item = TreeWidgetItem(self.treeWidget, self, drawable)
                self.treeWidget.addTopLevelItem(item)
        self.treeWidget.select_item(self.treeWidget.topLevelItemCount(), 0)
