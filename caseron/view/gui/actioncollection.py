#!/usr/bin/env python

import pathlib
from qtpy.QtWidgets import QAction
from qtpy.QtGui import QIcon
from qtpy.QtGui import QPixmap


class ActionCollection:
    def __init__(self, parent):
        self.icons_path = f'{pathlib.Path(__file__).parent}/UI/icons'

        # Actions
        self.action_show = QAction('&Show', parent)
        self.action_show = QAction('&Show', parent)
        self.action_hide = QAction('&Hide', parent)
        self.action_delete = QAction('&Delete', parent)
        self.action_center_camera = QAction('&Center camera', parent)
        self.action_highlight = QAction('T&oggle highlighting', parent)
        self.action_wireframe = QAction('&Toggle wireframe', parent)
        self.action_properties = QAction('&Properties', parent)
        self.action_colors = QAction('C&olors', parent)
        self.action_export_mesh = QAction('&Export mesh', parent)
        self.action_export_blocks = QAction('Export &blocks', parent)
        self.action_export_points = QAction('Export &points', parent)

        # Icons
        self.action_show.setIcon(QIcon(QPixmap(f'{self.icons_path}/flash_on.svg')))
        self.action_hide.setIcon(QIcon(QPixmap(f'{self.icons_path}/flash_off.svg')))
        self.action_delete.setIcon(QIcon(QPixmap(f'{self.icons_path}/cancel.svg')))
        self.action_center_camera.setIcon(QIcon(QPixmap(f'{self.icons_path}/collect.svg')))
        self.action_highlight.setIcon(QIcon(QPixmap(f'{self.icons_path}/idea.svg')))
        self.action_wireframe.setIcon(QIcon(QPixmap(f'{self.icons_path}/grid.svg')))
        self.action_properties.setIcon(QIcon(QPixmap(f'{self.icons_path}/settings.svg')))
        self.action_colors.setIcon(QIcon(QPixmap(f'{self.icons_path}/picture.svg')))
        self.action_export_mesh.setIcon(QIcon(QPixmap(f'{self.icons_path}/export.svg')))
        self.action_export_blocks.setIcon(QIcon(QPixmap(f'{self.icons_path}/export.svg')))
        self.action_export_points.setIcon(QIcon(QPixmap(f'{self.icons_path}/export.svg')))
