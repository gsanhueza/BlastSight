#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from datetime import datetime
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QAction

from .iconcollection import IconCollection
from .cameradialog import CameraDialog


class ActionCollection:
    def __init__(self, parent):
        # Tree Actions
        self.action_show = QAction('&Show', parent)
        self.action_show.setIcon(IconCollection.get('flash_on.svg'))

        self.action_hide = QAction('&Hide', parent)
        self.action_hide.setIcon(IconCollection.get('flash_off.svg'))

        self.action_delete = QAction('&Delete', parent)
        self.action_delete.setIcon(IconCollection.get('cancel.svg'))

        self.action_focus_camera = QAction('&Focus camera', parent)
        self.action_focus_camera.setIcon(IconCollection.get('collect.svg'))

        self.action_highlight = QAction('H&ighlight', parent)
        self.action_highlight.setIcon(IconCollection.get('idea.svg'))
        self.action_highlight.setCheckable(True)

        self.action_wireframe = QAction('&Wireframe', parent)
        self.action_wireframe.setIcon(IconCollection.get('grid.svg'))
        self.action_wireframe.setCheckable(True)

        self.action_properties = QAction('&Properties', parent)
        self.action_properties.setIcon(IconCollection.get('settings.svg'))

        self.action_setup_colors = QAction('Setup c&olors', parent)
        self.action_setup_colors.setIcon(IconCollection.get('picture.svg'))

        self.action_export_mesh = QAction('&Export mesh', parent)
        self.action_export_mesh.setIcon(IconCollection.get('export.svg'))

        self.action_export_blocks = QAction('Export &blocks', parent)
        self.action_export_blocks.setIcon(IconCollection.get('export.svg'))

        self.action_export_points = QAction('Export &points', parent)
        self.action_export_points.setIcon(IconCollection.get('export.svg'))

        self.action_export_lines = QAction('Export &lines', parent)
        self.action_export_lines.setIcon(IconCollection.get('export.svg'))

        self.action_export_tubes = QAction('Export &tubes', parent)
        self.action_export_tubes.setIcon(IconCollection.get('export.svg'))

        # MainWindow Actions
        self.action_load_mesh = QAction('Load &mesh', parent)
        self.action_load_mesh.setIcon(IconCollection.get('area_chart.svg'))
        self.action_load_mesh.setShortcut('Ctrl+A')

        self.action_load_blocks = QAction('Load &blocks', parent)
        self.action_load_blocks.setIcon(IconCollection.get('data_sheet.svg'))
        self.action_load_blocks.setShortcut('Ctrl+E')

        self.action_load_points = QAction('Load &points', parent)
        self.action_load_points.setIcon(IconCollection.get('scatter_plot.svg'))
        self.action_load_points.setShortcut('Ctrl+P')

        self.action_load_lines = QAction('Load &lines', parent)
        self.action_load_lines.setIcon(IconCollection.get('line_chart.svg'))
        self.action_load_lines.setShortcut('Ctrl+L')

        self.action_load_tubes = QAction('Load &tubes', parent)
        self.action_load_tubes.setIcon(IconCollection.get('radar_plot.svg'))
        self.action_load_tubes.setShortcut('Ctrl+T')

        self.action_load_mesh_folder = QAction('Load m&esh folder', parent)
        self.action_load_mesh_folder.setIcon(IconCollection.get('area_chart.svg'))
        self.action_load_mesh_folder.setShortcut('Ctrl+Shift+A')

        self.action_load_blocks_folder = QAction('Load b&locks folder', parent)
        self.action_load_blocks_folder.setIcon(IconCollection.get('data_sheet.svg'))
        self.action_load_blocks_folder.setShortcut('Ctrl+Shift+E')

        self.action_load_points_folder = QAction('Load p&oints folder', parent)
        self.action_load_points_folder.setIcon(IconCollection.get('scatter_plot.svg'))
        self.action_load_points_folder.setShortcut('Ctrl+Shift+P')

        self.action_load_lines_folder = QAction('Load l&ines folder', parent)
        self.action_load_lines_folder.setIcon(IconCollection.get('line_chart.svg'))
        self.action_load_lines_folder.setShortcut('Ctrl+Shift+L')

        self.action_load_tubes_folder = QAction('Load t&ubes folder', parent)
        self.action_load_tubes_folder.setIcon(IconCollection.get('radar_plot.svg'))
        self.action_load_tubes_folder.setShortcut('Ctrl+Shift+T')

        self.action_quit = QAction('&Quit', parent)
        self.action_quit.setIcon(IconCollection.get('cancel.svg'))
        self.action_quit.setShortcut('Ctrl+Q')

        self.action_show_tree = QAction('Show &tree', parent)
        self.action_show_tree.setIcon(IconCollection.get('list.svg'))
        self.action_show_tree.setShortcut('Ctrl+W')

        self.action_help = QAction('&Help', parent)
        self.action_help.setIcon(IconCollection.get('document.svg'))
        self.action_help.setShortcut('F1')

        self.action_about = QAction('&About', parent)
        self.action_about.setIcon(IconCollection.get('about.svg'))
        self.action_about.setShortcut('?')

        self.action_turbo_rendering = QAction('Tur&bo rendering', parent)
        self.action_turbo_rendering.setIcon(IconCollection.get('sports_mode.svg'))
        self.action_turbo_rendering.setShortcut('Ctrl+Shift+R')
        self.action_turbo_rendering.setCheckable(True)

        self.action_normal_mode = QAction('Return to &normal', parent)
        self.action_normal_mode.setIcon(IconCollection.get('rotate_camera.svg'))
        self.action_normal_mode.setShortcut('Ctrl+N')

        self.action_slice_mode = QAction('&Slice meshes/blocks', parent)
        self.action_slice_mode.setIcon(IconCollection.get('flash_on.svg'))
        self.action_slice_mode.setShortcut('Ctrl+S')

        self.action_measurement_mode = QAction('&Measure mesh distances', parent)
        self.action_measurement_mode.setIcon(IconCollection.get('ruler.svg'))
        self.action_measurement_mode.setShortcut('Ctrl+M')

        self.action_detection_mode = QAction('&Detect meshes', parent)
        self.action_detection_mode.setIcon(IconCollection.get('cursor.svg'))
        self.action_detection_mode.setShortcut('Ctrl+D')

        self.action_camera_properties = QAction('&Camera properties', parent)
        self.action_camera_properties.setIcon(IconCollection.get('compact_camera.svg'))
        self.action_camera_properties.setShortcut('Ctrl+C')

        self.action_plan_view = QAction('&Plan view', parent)
        self.action_plan_view.setIcon(IconCollection.get('upload.svg'))
        self.action_plan_view.setShortcut('Ctrl+1')

        self.action_north_view = QAction('&North view', parent)
        self.action_north_view.setIcon(IconCollection.get('up.svg'))
        self.action_north_view.setShortcut('Ctrl+2')

        self.action_east_view = QAction('&East view', parent)
        self.action_east_view.setIcon(IconCollection.get('right.svg'))
        self.action_east_view.setShortcut('Ctrl+3')

        self.action_fit_to_screen = QAction('&Fit to screen', parent)
        self.action_fit_to_screen.setIcon(IconCollection.get('collect.svg'))
        self.action_fit_to_screen.setShortcut('Ctrl+F')

        self.action_autofit_to_screen = QAction('&Auto-fit to screen', parent)
        self.action_autofit_to_screen.setIcon(IconCollection.get('globe.svg'))
        self.action_autofit_to_screen.setShortcut('Ctrl+Shift+F')
        self.action_autofit_to_screen.setCheckable(True)

        self.action_perspective_projection = QAction('P&erspective projection', parent)
        self.action_perspective_projection.setIcon(IconCollection.get('ruler.svg'))
        self.action_perspective_projection.setShortcut('Ctrl+4')

        self.action_orthographic_projection = QAction('O&rthographic projection', parent)
        self.action_orthographic_projection.setIcon(IconCollection.get('ruler.svg'))
        self.action_orthographic_projection.setShortcut('Ctrl+5')

        self.action_take_screenshot = QAction('&Take screenshot', parent)
        self.action_take_screenshot.setIcon(IconCollection.get('webcam.svg'))
        self.action_take_screenshot.setShortcut('Ctrl+Shift+S')

    """
    Basic handlers
    """
    def connect_tree(self, tree) -> None:
        self.action_show_tree.triggered.connect(tree.show)

    def connect_main_widget(self, widget) -> None:
        self.action_quit.triggered.connect(widget.close)

    def connect_viewer(self, viewer) -> None:
        self.action_plan_view.triggered.connect(viewer.plan_view)
        self.action_north_view.triggered.connect(viewer.north_view)
        self.action_east_view.triggered.connect(viewer.east_view)
        self.action_fit_to_screen.triggered.connect(viewer.fit_to_screen)

        self.action_autofit_to_screen.triggered.connect(viewer.set_autofit_status)
        self.action_turbo_rendering.triggered.connect(viewer.set_turbo_status)

        self.action_camera_properties.triggered.connect(lambda: ActionCollection.handle_camera(viewer))
        self.action_take_screenshot.triggered.connect(lambda: ActionCollection.handle_screenshot(viewer))

        viewer.signal_load_success.connect(viewer.update_turbo)
        viewer.signal_load_success.connect(viewer.update_autofit)

    """
    Advanced handlers
    """
    @staticmethod
    def handle_camera(viewer) -> None:
        dialog = CameraDialog(viewer)
        dialog.accepted.connect(lambda: ActionCollection.update_viewer(viewer, dialog))
        dialog.show()

    @staticmethod
    def update_viewer(viewer, dialog: CameraDialog) -> None:
        viewer.camera_position = dialog.camera_position
        viewer.rotation_angle = dialog.rotation_angle
        viewer.rotation_center = dialog.rotation_center
        viewer.update()

    @staticmethod
    def handle_screenshot(viewer) -> None:
        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=viewer,
            directory=f'BlastSight Screenshot ({datetime.now().strftime("%Y%m%d-%H%M%S")})',
            filter='PNG image (*.png);;')

        if path != '':
            viewer.take_screenshot(path)
