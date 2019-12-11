#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from datetime import datetime
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QAction
from qtpy.QtGui import QIcon

from .cameradialog import CameraDialog


class ActionCollection:
    def __init__(self, parent):
        self.icons_path = f'{pathlib.Path(__file__).parent}/UI/icons'

        # Tree Actions
        self.action_show = QAction('&Show', parent)
        self.action_show.setIcon(QIcon(f'{self.icons_path}/flash_on.svg'))

        self.action_hide = QAction('&Hide', parent)
        self.action_hide.setIcon(QIcon(f'{self.icons_path}/flash_off.svg'))

        self.action_delete = QAction('&Delete', parent)
        self.action_delete.setIcon(QIcon(f'{self.icons_path}/cancel.svg'))

        self.action_focus_camera = QAction('&Focus camera', parent)
        self.action_focus_camera.setIcon(QIcon(f'{self.icons_path}/collect.svg'))

        self.action_highlight = QAction('H&ighlight', parent)
        self.action_highlight.setIcon(QIcon(f'{self.icons_path}/idea.svg'))
        self.action_highlight.setCheckable(True)

        self.action_wireframe = QAction('&Wireframe', parent)
        self.action_wireframe.setIcon(QIcon(f'{self.icons_path}/grid.svg'))
        self.action_wireframe.setCheckable(True)

        self.action_properties = QAction('&Properties', parent)
        self.action_properties.setIcon(QIcon(f'{self.icons_path}/settings.svg'))

        self.action_setup_colors = QAction('Setup c&olors', parent)
        self.action_setup_colors.setIcon(QIcon(f'{self.icons_path}/picture.svg'))

        self.action_export_mesh = QAction('&Export mesh', parent)
        self.action_export_mesh.setIcon(QIcon(f'{self.icons_path}/export.svg'))

        self.action_export_blocks = QAction('Export &blocks', parent)
        self.action_export_blocks.setIcon(QIcon(f'{self.icons_path}/export.svg'))

        self.action_export_points = QAction('Export &points', parent)
        self.action_export_points.setIcon(QIcon(f'{self.icons_path}/export.svg'))

        self.action_export_lines = QAction('Export &lines', parent)
        self.action_export_lines.setIcon(QIcon(f'{self.icons_path}/export.svg'))

        self.action_export_tubes = QAction('Export &tubes', parent)
        self.action_export_tubes.setIcon(QIcon(f'{self.icons_path}/export.svg'))

        # MainWindow Actions
        self.action_load_mesh = QAction('Load &mesh', parent)
        self.action_load_mesh.setIcon(QIcon(f'{self.icons_path}/area_chart.svg'))
        self.action_load_mesh.setShortcut('Ctrl+A')

        self.action_load_blocks = QAction('Load &blocks', parent)
        self.action_load_blocks.setIcon(QIcon(f'{self.icons_path}/data_sheet.svg'))
        self.action_load_blocks.setShortcut('Ctrl+E')

        self.action_load_points = QAction('Load &points', parent)
        self.action_load_points.setIcon(QIcon(f'{self.icons_path}/scatter_plot.svg'))
        self.action_load_points.setShortcut('Ctrl+P')

        self.action_load_lines = QAction('Load &lines', parent)
        self.action_load_lines.setIcon(QIcon(f'{self.icons_path}/line_chart.svg'))
        self.action_load_lines.setShortcut('Ctrl+L')

        self.action_load_tubes = QAction('Load &tubes', parent)
        self.action_load_tubes.setIcon(QIcon(f'{self.icons_path}/radar_plot.svg'))
        self.action_load_tubes.setShortcut('Ctrl+U')

        self.action_load_mesh_folder = QAction('Load m&esh folder', parent)
        self.action_load_mesh_folder.setIcon(QIcon(f'{self.icons_path}/area_chart.svg'))
        self.action_load_mesh_folder.setShortcut('Ctrl+Shift+A')

        self.action_load_blocks_folder = QAction('Load b&locks folder', parent)
        self.action_load_blocks_folder.setIcon(QIcon(f'{self.icons_path}/data_sheet.svg'))
        self.action_load_blocks_folder.setShortcut('Ctrl+Shift+E')

        self.action_load_points_folder = QAction('Load p&oints folder', parent)
        self.action_load_points_folder.setIcon(QIcon(f'{self.icons_path}/scatter_plot.svg'))
        self.action_load_points_folder.setShortcut('Ctrl+Shift+P')

        self.action_load_lines_folder = QAction('Load l&ines folder', parent)
        self.action_load_lines_folder.setIcon(QIcon(f'{self.icons_path}/line_chart.svg'))
        self.action_load_lines_folder.setShortcut('Ctrl+Shift+L')

        self.action_load_tubes_folder = QAction('Load t&ubes folder', parent)
        self.action_load_tubes_folder.setIcon(QIcon(f'{self.icons_path}/radar_plot.svg'))
        self.action_load_tubes_folder.setShortcut('Ctrl+Shift+U')

        self.action_quit = QAction('&Quit', parent)
        self.action_quit.setIcon(QIcon(f'{self.icons_path}/cancel.svg'))
        self.action_quit.setShortcut('Ctrl+Q')

        self.action_show_tree = QAction('Show &tree', parent)
        self.action_show_tree.setIcon(QIcon(f'{self.icons_path}/list.svg'))
        self.action_show_tree.setShortcut('Ctrl+W')

        self.action_help = QAction('&Help', parent)
        self.action_help.setIcon(QIcon(f'{self.icons_path}/document.svg'))
        self.action_help.setShortcut('F1')

        self.action_about = QAction('&About', parent)
        self.action_about.setIcon(QIcon(f'{self.icons_path}/about.svg'))
        self.action_about.setShortcut('?')

        self.action_turbo_rendering = QAction('Tur&bo rendering', parent)
        self.action_turbo_rendering.setIcon(QIcon(f'{self.icons_path}/sports_mode.svg'))
        self.action_turbo_rendering.setShortcut('Ctrl+B')
        self.action_turbo_rendering.setCheckable(True)

        self.action_normal_mode = QAction('Return to &normal', parent)
        self.action_normal_mode.setIcon(QIcon(f'{self.icons_path}/rotate_camera.svg'))
        self.action_normal_mode.setShortcut('Ctrl+N')

        self.action_slice_mode = QAction('&Slice meshes/blocks', parent)
        self.action_slice_mode.setIcon(QIcon(f'{self.icons_path}/flash_on.svg'))
        self.action_slice_mode.setShortcut('Ctrl+S')

        self.action_measurement_mode = QAction('&Measure mesh distances', parent)
        self.action_measurement_mode.setIcon(QIcon(f'{self.icons_path}/ruler.svg'))
        self.action_measurement_mode.setShortcut('Ctrl+M')

        self.action_detection_mode = QAction('&Detect meshes', parent)
        self.action_detection_mode.setIcon(QIcon(f'{self.icons_path}/cursor.svg'))
        self.action_detection_mode.setShortcut('Ctrl+D')

        self.action_camera_properties = QAction('&Camera properties', parent)
        self.action_camera_properties.setIcon(QIcon(f'{self.icons_path}/compact_camera.svg'))
        self.action_camera_properties.setShortcut('Ctrl+C')

        self.action_plan_view = QAction('&Plan view', parent)
        self.action_plan_view.setIcon(QIcon(f'{self.icons_path}/upload.svg'))
        self.action_plan_view.setShortcut('Ctrl+1')

        self.action_north_view = QAction('&North view', parent)
        self.action_north_view.setIcon(QIcon(f'{self.icons_path}/up.svg'))
        self.action_north_view.setShortcut('Ctrl+2')

        self.action_east_view = QAction('&East view', parent)
        self.action_east_view.setIcon(QIcon(f'{self.icons_path}/right.svg'))
        self.action_east_view.setShortcut('Ctrl+3')

        self.action_fit_to_screen = QAction('&Fit to screen', parent)
        self.action_fit_to_screen.setIcon(QIcon(f'{self.icons_path}/collect.svg'))
        self.action_fit_to_screen.setShortcut('Ctrl+F')

        self.action_autofit_to_screen = QAction('&Auto-fit to screen', parent)
        self.action_autofit_to_screen.setIcon(QIcon(f'{self.icons_path}/globe.svg'))
        self.action_autofit_to_screen.setShortcut('Ctrl+Shift+F')
        self.action_autofit_to_screen.setCheckable(True)
        self.action_autofit_to_screen.setChecked(True)

        self.action_perspective_projection = QAction('P&erspective projection', parent)
        self.action_perspective_projection.setIcon(QIcon(f'{self.icons_path}/ruler.svg'))
        self.action_perspective_projection.setShortcut('Ctrl+4')

        self.action_orthographic_projection = QAction('O&rthographic projection', parent)
        self.action_orthographic_projection.setIcon(QIcon(f'{self.icons_path}/ruler.svg'))
        self.action_orthographic_projection.setShortcut('Ctrl+5')

        self.action_take_screenshot = QAction('&Take screenshot', parent)
        self.action_take_screenshot.setIcon(QIcon(f'{self.icons_path}/webcam.svg'))
        self.action_take_screenshot.setShortcut('Ctrl+T')

    """
    Basic handlers
    """
    def connect_tree(self, tree):
        self.action_show_tree.triggered.connect(tree.show)

    def connect_main_widget(self, widget):
        self.action_quit.triggered.connect(widget.close)

    def connect_viewer(self, viewer):
        self.action_plan_view.triggered.connect(viewer.plan_view)
        self.action_north_view.triggered.connect(viewer.north_view)
        self.action_east_view.triggered.connect(viewer.east_view)
        self.action_fit_to_screen.triggered.connect(viewer.fit_to_screen)

        self.action_autofit_to_screen.triggered.connect(
            lambda: self.handle_autofit(viewer))
        self.action_turbo_rendering.triggered.connect(
            lambda: self.handle_turbo(viewer))
        self.action_camera_properties.triggered.connect(
            lambda: self.handle_camera_properties(viewer))
        self.action_take_screenshot.triggered.connect(
            lambda: self.handle_screenshot(viewer))

        viewer.signal_file_modified.connect(
            lambda: self.handle_turbo(viewer))
        viewer.signal_load_success.connect(
            lambda: self.handle_autofit(viewer))

    """
    Advanced handlers
    """
    def handle_autofit(self, viewer):
        viewer.autofit_to_screen = self.action_autofit_to_screen.isChecked()

    def handle_turbo(self, viewer):
        viewer.turbo_rendering = self.action_turbo_rendering.isChecked()

    def handle_camera_properties(self, viewer):
        dialog = CameraDialog(viewer)
        dialog.show()

    def handle_screenshot(self, viewer):
        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=viewer,
            directory=f'BlastSight Screenshot ({datetime.now().strftime("%Y%m%d-%H%M%S")})',
            filter='PNG image (*.png);;')

        if path != '':
            viewer.take_screenshot(path)
