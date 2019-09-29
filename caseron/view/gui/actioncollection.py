#!/usr/bin/env python

import pathlib
from qtpy.QtCore import QCoreApplication
from qtpy.QtWidgets import QAction
from qtpy.QtGui import QIcon
from qtpy.QtGui import QPixmap


class ActionCollection:
    def __init__(self, parent):
        self.icons_path = f'{pathlib.Path(__file__).parent}/UI/icons'

        # Tree Actions
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

        # MainWindow Actions
        self.action_load_mesh = QAction('Load &mesh', parent)
        self.action_load_blocks = QAction('Load &blocks', parent)
        self.action_load_points = QAction('Load &points', parent)
        self.action_load_mesh_folder = QAction('Load m&esh folder', parent)
        self.action_load_blocks_folder = QAction('Load b&locks folder', parent)
        self.action_load_points_folder = QAction('Load p&oints folder', parent)
        self.action_quit = QAction('&Quit', parent)
        self.action_show_tree = QAction('Show &tree', parent)
        self.action_help = QAction('&Help', parent)
        self.action_about = QAction('&About', parent)
        self.action_normal_mode = QAction('Return to &normal', parent)
        self.action_slice_mode = QAction('&Slice meshes', parent)
        self.action_measurement_mode = QAction('&Measure distance (in mesh)', parent)
        self.action_detection_mode = QAction('&Detect meshes', parent)
        self.action_camera_properties = QAction('&Camera properties', parent)
        self.action_plan_view = QAction('&Plan view', parent)
        self.action_north_view = QAction('&North view', parent)
        self.action_east_view = QAction('&East view', parent)
        self.action_fit_to_screen = QAction('&Fit to screen', parent)
        self.action_perspective_projection = QAction('P&erspective projection', parent)
        self.action_orthographic_projection = QAction('O&rthographic projection', parent)
        self.action_take_screenshot = QAction('&Take screenshot', parent)

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

        self.action_show_tree.setIcon(QIcon(QPixmap(f'{self.icons_path}/list.svg')))
        self.action_load_mesh.setIcon(QIcon(QPixmap(f'{self.icons_path}/radar_plot.svg')))
        self.action_load_blocks.setIcon(QIcon(QPixmap(f'{self.icons_path}/data_sheet.svg')))
        self.action_load_points.setIcon(QIcon(QPixmap(f'{self.icons_path}/scatter_plot.svg')))
        self.action_load_mesh_folder.setIcon(QIcon(QPixmap(f'{self.icons_path}/radar_plot.svg')))
        self.action_load_blocks_folder.setIcon(QIcon(QPixmap(f'{self.icons_path}/data_sheet.svg')))
        self.action_load_points_folder.setIcon(QIcon(QPixmap(f'{self.icons_path}/scatter_plot.svg')))
        self.action_quit.setIcon(QIcon(QPixmap(f'{self.icons_path}/cancel.svg')))
        self.action_show_tree.setIcon(QIcon(QPixmap(f'{self.icons_path}/list.svg')))
        self.action_help.setIcon(QIcon(QPixmap(f'{self.icons_path}/document.svg')))
        self.action_about.setIcon(QIcon(QPixmap(f'{self.icons_path}/about.svg')))
        self.action_normal_mode.setIcon(QIcon(QPixmap(f'{self.icons_path}/rotate_camera.svg')))
        self.action_slice_mode.setIcon(QIcon(QPixmap(f'{self.icons_path}/flash_on.svg')))
        self.action_measurement_mode.setIcon(QIcon(QPixmap(f'{self.icons_path}/ruler.svg')))
        self.action_detection_mode.setIcon(QIcon(QPixmap(f'{self.icons_path}/cursor.svg')))
        self.action_camera_properties.setIcon(QIcon(QPixmap(f'{self.icons_path}/compact_camera.svg')))
        self.action_plan_view.setIcon(QIcon(QPixmap(f'{self.icons_path}/upload.svg')))
        self.action_north_view.setIcon(QIcon(QPixmap(f'{self.icons_path}/up.svg')))
        self.action_east_view.setIcon(QIcon(QPixmap(f'{self.icons_path}/right.svg')))
        self.action_fit_to_screen.setIcon(QIcon(QPixmap(f'{self.icons_path}/globe.svg')))
        self.action_perspective_projection.setIcon(QIcon(QPixmap(f'{self.icons_path}/ruler.svg')))
        self.action_orthographic_projection.setIcon(QIcon(QPixmap(f'{self.icons_path}/ruler.svg')))
        self.action_take_screenshot.setIcon(QIcon(QPixmap(f'{self.icons_path}/webcam.svg')))

        # Shortcuts
        _translate = QCoreApplication.translate
        self.action_load_mesh.setShortcut(_translate("self", "Ctrl+A"))
        self.action_load_mesh_folder.setShortcut(_translate("self", "Ctrl+Shift+A"))
        self.action_load_blocks_folder.setShortcut(_translate("self", "Ctrl+Shift+E"))
        self.action_load_points_folder.setShortcut(_translate("self", "Ctrl+Shift+P"))
        self.action_quit.setShortcut(_translate("self", "Ctrl+Q"))
        self.action_show_tree.setShortcut(_translate("self", "Ctrl+W"))
        self.action_help.setShortcut(_translate("self", "F1"))
        self.action_about.setShortcut(_translate("self", "?"))
        self.action_normal_mode.setShortcut(_translate("self", "Ctrl+N"))
        self.action_slice_mode.setShortcut(_translate("self", "Ctrl+S"))
        self.action_measurement_mode.setShortcut(_translate("self", "Ctrl+M"))
        self.action_load_blocks.setShortcut(_translate("self", "Ctrl+E"))
        self.action_detection_mode.setShortcut(_translate("self", "Ctrl+D"))
        self.action_camera_properties.setShortcut(_translate("self", "Ctrl+C"))
        self.action_load_points.setShortcut(_translate("self", "Ctrl+P"))
        self.action_plan_view.setShortcut(_translate("self", "Ctrl+1"))
        self.action_north_view.setShortcut(_translate("self", "Ctrl+2"))
        self.action_east_view.setShortcut(_translate("self", "Ctrl+3"))
        self.action_fit_to_screen.setShortcut(_translate("self", "Ctrl+R"))
        self.action_perspective_projection.setShortcut(_translate("self", "Ctrl+4"))
        self.action_orthographic_projection.setShortcut(_translate("self", "Ctrl+5"))
        self.action_take_screenshot.setShortcut(_translate("self", "Ctrl+T"))
