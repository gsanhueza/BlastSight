#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
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

    def auto_connect(self, tree, viewer) -> None:
        self.connect_tree(tree)
        self.connect_viewer(viewer)
        tree.connect_viewer(viewer)

    def connect_tree(self, tree) -> None:
        actions = self.action_collection
        actions.action_show_tree.triggered.connect(tree.show)

    def connect_viewer(self, viewer) -> None:
        actions = self.action_collection
        actions.action_plan_view.triggered.connect(viewer.plan_view)
        actions.action_north_view.triggered.connect(viewer.north_view)
        actions.action_east_view.triggered.connect(viewer.east_view)
        actions.action_fit_to_screen.triggered.connect(viewer.fit_to_screen)

        actions.action_autofit_to_screen.triggered.connect(viewer.set_autofit_status)
        actions.action_animated_viewer.triggered.connect(viewer.set_animated_status)
        actions.action_turbo_rendering.triggered.connect(viewer.set_turbo_status)

        actions.action_perspective_projection.triggered.connect(viewer.perspective_projection)
        actions.action_orthographic_projection.triggered.connect(viewer.orthographic_projection)
