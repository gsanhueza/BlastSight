#!/usr/bin/env python

from qtpy.QtWidgets import QToolBar

from .actioncollection import ActionCollection


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        QToolBar.__init__(self, parent)
        self.setAcceptDrops(True)

        self.actions = ActionCollection(self)
        self.add_actions()

    def add_actions(self):
        self.addAction(self.actions.action_show_tree)
        self.addSeparator()
        self.addAction(self.actions.action_plan_view)
        self.addAction(self.actions.action_north_view)
        self.addAction(self.actions.action_east_view)
        self.addAction(self.actions.action_fit_to_screen)
        self.addSeparator()
        self.addAction(self.actions.action_take_screenshot)

    def connect_tree(self, tree):
        self.actions.action_show_tree.triggered.connect(tree.show)

    def connect_viewer(self, viewer):
        self.actions.action_plan_view.triggered.connect(viewer.plan_view)
        self.actions.action_north_view.triggered.connect(viewer.north_view)
        self.actions.action_east_view.triggered.connect(viewer.east_view)
        self.actions.action_fit_to_screen.triggered.connect(viewer.fit_to_screen)
        self.actions.action_take_screenshot.triggered.connect(viewer.take_screenshot)
