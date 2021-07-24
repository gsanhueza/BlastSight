#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtWidgets import QToolBar
from .actioncollection import ActionCollection


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        QToolBar.__init__(self, parent)
        self.setAcceptDrops(True)

        self.action_collection = ActionCollection(self)
        self.add_actions()

    def add_actions(self) -> None:
        self.addAction(self.action_collection.action_show_tree)
        self.addAction(self.action_collection.action_viewer_properties)
        self.addSeparator()
        self.addAction(self.action_collection.action_plan_view)
        self.addAction(self.action_collection.action_north_view)
        self.addAction(self.action_collection.action_east_view)
        self.addAction(self.action_collection.action_fit_to_screen)
        self.addSeparator()
        self.addAction(self.action_collection.action_autofit)
        self.addAction(self.action_collection.action_turbo_rendering)
        self.addSeparator()
        self.addAction(self.action_collection.action_xsection)
        self.addAction(self.action_collection.action_grid)
        self.addAction(self.action_collection.action_take_screenshot)

    def auto_connect(self, tree, viewer, camera, xsection, grid) -> None:
        self.connect_tree(tree)
        self.connect_viewer(viewer)
        self.connect_camera(camera)
        self.connect_xsection(xsection)
        self.connect_grid(grid)

        tree.connect_viewer(viewer)
        camera.connect_viewer(viewer)
        xsection.connect_viewer(viewer)
        grid.connect_viewer(viewer)

    def connect_tree(self, tree) -> None:
        actions = self.action_collection
        actions.action_show_tree.triggered.connect(tree.show)

    def connect_camera(self, camera):
        actions = self.action_collection
        actions.action_viewer_properties.triggered.connect(camera.show)

    def connect_xsection(self, xsection):
        actions = self.action_collection
        actions.action_xsection.triggered.connect(xsection.show)

    def connect_grid(self, grid):
        actions = self.action_collection
        actions.action_grid.triggered.connect(grid.show)

    def connect_viewer(self, viewer) -> None:
        actions = self.action_collection
        actions.action_plan_view.triggered.connect(viewer.plan_view)
        actions.action_north_view.triggered.connect(viewer.north_view)
        actions.action_east_view.triggered.connect(viewer.east_view)
        actions.action_fit_to_screen.triggered.connect(viewer.fit_to_screen)

        actions.action_perspective_projection.triggered.connect(viewer.perspective_projection)
        actions.action_orthographic_projection.triggered.connect(viewer.orthographic_projection)

        # React to viewer changes ourselves, since blastsight>=0.5.1 will not auto-do it anymore
        def auto_fit() -> None:
            if actions.action_autofit.isChecked():
                viewer.fit_to_screen()

        def auto_turbo() -> None:
            viewer.set_turbo_rendering(actions.action_turbo_rendering.isChecked())

        def animated() -> None:
            viewer.is_animated = actions.action_animated.isChecked()

        actions.action_animated.triggered.connect(animated)
        actions.action_autofit.triggered.connect(auto_fit)
        actions.action_turbo_rendering.triggered.connect(auto_turbo)

        viewer.signal_file_modified.connect(auto_fit)
        viewer.signal_load_success.connect(auto_turbo)
