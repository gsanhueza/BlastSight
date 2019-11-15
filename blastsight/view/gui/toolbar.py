#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
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

    def add_actions(self):
        self.addAction(self.action_collection.action_show_tree)
        self.addSeparator()
        self.addAction(self.action_collection.action_plan_view)
        self.addAction(self.action_collection.action_north_view)
        self.addAction(self.action_collection.action_east_view)
        self.addAction(self.action_collection.action_fit_to_screen)
        self.addSeparator()
        self.addAction(self.action_collection.action_turbo_rendering)
        self.addAction(self.action_collection.action_take_screenshot)

    def connect_tree(self, tree):
        self.action_collection.action_show_tree.triggered.connect(tree.show)

    def connect_viewer(self, viewer):
        self.action_collection.action_plan_view.triggered.connect(viewer.plan_view)
        self.action_collection.action_north_view.triggered.connect(viewer.north_view)
        self.action_collection.action_east_view.triggered.connect(viewer.east_view)
        self.action_collection.action_fit_to_screen.triggered.connect(viewer.fit_to_screen)
        self.action_collection.action_take_screenshot.triggered.connect(viewer.take_screenshot)
