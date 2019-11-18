#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from datetime import datetime
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QToolBar

from .actioncollection import ActionCollection
from .cameradialog import CameraDialog


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        QToolBar.__init__(self, parent)
        self.setAcceptDrops(True)

        self.action_collection = ActionCollection(self)
        self.add_actions()

    def add_actions(self):
        self.addAction(self.action_collection.action_show_tree)
        self.addSeparator()
        self.addAction(self.action_collection.action_plan_view)
        self.addAction(self.action_collection.action_north_view)
        self.addAction(self.action_collection.action_east_view)
        self.addAction(self.action_collection.action_fit_to_screen)
        self.addSeparator()
        self.addAction(self.action_collection.action_autofit_to_screen)
        self.addAction(self.action_collection.action_turbo_rendering)
        self.addSeparator()
        self.addAction(self.action_collection.action_take_screenshot)

    def connect_tree(self, tree):
        self.action_collection.action_show_tree.triggered.connect(tree.show)

    def connect_viewer(self, viewer):
        self.action_collection.action_plan_view.triggered.connect(viewer.plan_view)
        self.action_collection.action_north_view.triggered.connect(viewer.north_view)
        self.action_collection.action_east_view.triggered.connect(viewer.east_view)
        self.action_collection.action_fit_to_screen.triggered.connect(viewer.fit_to_screen)

        self.action_collection.action_autofit_to_screen.triggered.connect(
            lambda: self.handle_autofit(viewer))
        self.action_collection.action_turbo_rendering.triggered.connect(
            lambda: self.handle_turbo(viewer))
        self.action_collection.action_camera_properties.triggered.connect(
            lambda: self.dialog_camera(viewer))
        self.action_collection.action_take_screenshot.triggered.connect(
            lambda: self.dialog_screenshot(viewer))

        viewer.signal_file_modified.connect(
            lambda: self.handle_turbo(viewer))
        viewer.signal_load_success.connect(
            lambda: self.handle_autofit(viewer))

    def connect_main_widget(self, widget):
        self.action_collection.action_quit.triggered.connect(widget.close)

    """
    Advanced handlers
    """
    def handle_autofit(self, viewer):
        viewer.autofit_to_screen = self.action_collection.action_autofit_to_screen.isChecked()

    def handle_turbo(self, viewer):
        viewer.turbo_rendering = self.action_collection.action_turbo_rendering.isChecked()

    def dialog_camera(self, viewer):
        dialog = CameraDialog(viewer)
        dialog.show()

    def dialog_screenshot(self, viewer):
        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self,
            directory=f'BlastSight Screenshot ({datetime.now().strftime("%Y%m%d-%H%M%S")})',
            filter='PNG image (*.png);;')

        if path != '':
            viewer.take_screenshot(path)
