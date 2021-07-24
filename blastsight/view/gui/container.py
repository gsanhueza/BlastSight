#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from datetime import datetime

from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

from .camerawidget import CameraWidget
from .gridwidget import GridWidget
from .toolbar import ToolBar
from .treewidget import TreeWidget
from .xsectionwidget import XSectionWidget

from .iconcollection import IconCollection
from ..integrableviewer import IntegrableViewer


class Container(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        # Container
        self.setWindowTitle('BlastSight (Container)')
        self.resize(600, 500)

        # Widgets
        self.toolbar = ToolBar(self)
        self.viewer = IntegrableViewer(self)
        self.camera = CameraWidget()
        self.tree = TreeWidget()
        self.xsection = XSectionWidget()
        self.grid = GridWidget()

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.viewer)
        self.layout.addWidget(self.toolbar)

        # Actions
        self.toolbar.auto_connect(self.tree, self.viewer, self.camera, self.xsection, self.grid)

        actions = self.toolbar.action_collection
        actions.action_take_screenshot.triggered.connect(self.handle_screenshot)

        # Icons
        try:
            self.set_widgets_icon(parent.windowIcon())
        except AttributeError:
            self.set_widgets_icon(IconCollection.get('blastsight.png'))

    def set_widgets_icon(self, icon) -> None:
        self.setWindowIcon(icon)
        self.camera.setWindowIcon(icon)
        self.tree.setWindowIcon(icon)

    def handle_screenshot(self) -> None:
        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self.viewer,
            directory=f'BlastSight Screenshot ({datetime.now().strftime("%Y%m%d-%H%M%S")})',
            filter='PNG image (*.png);;')

        self.viewer.take_screenshot(path)

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
