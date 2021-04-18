#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtWidgets import QAction

from .iconcollection import IconCollection


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

        self.action_setup_multiple = QAction('Setup &multiple', parent)
        self.action_setup_multiple.setIcon(IconCollection.get('picture.svg'))

        self.action_export_element = QAction('&Export', parent)
        self.action_export_element.setIcon(IconCollection.get('export.svg'))

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

        self.action_animated = QAction('A&nimate movements', parent)
        self.action_animated.setIcon(IconCollection.get('film_reel.svg'))
        self.action_animated.setShortcut('Shift+N')
        self.action_animated.setCheckable(True)

        self.action_autofit = QAction('&Auto-fit to screen', parent)
        self.action_autofit.setIcon(IconCollection.get('globe.svg'))
        self.action_autofit.setShortcut('Shift+F')
        self.action_autofit.setCheckable(True)

        self.action_autorotate = QAction('Auto-&rotate on slice', parent)
        self.action_autorotate.setIcon(IconCollection.get('process.svg'))
        self.action_autorotate.setShortcut('Shift+R')
        self.action_autorotate.setCheckable(True)

        self.action_turbo_rendering = QAction('&Turbo rendering', parent)
        self.action_turbo_rendering.setIcon(IconCollection.get('sports_mode.svg'))
        self.action_turbo_rendering.setShortcut('Shift+T')
        self.action_turbo_rendering.setCheckable(True)

        self.action_normal_controller = QAction('&Normal controller', parent)
        self.action_normal_controller.setIcon(IconCollection.get('rotate_camera.svg'))
        self.action_normal_controller.setShortcut('Ctrl+N')

        self.action_measurement_controller = QAction('&Measure meshes', parent)
        self.action_measurement_controller.setIcon(IconCollection.get('ruler.svg'))
        self.action_measurement_controller.setShortcut('Ctrl+M')

        self.action_detection_controller = QAction('&Detect meshes/lines', parent)
        self.action_detection_controller.setIcon(IconCollection.get('cursor.svg'))
        self.action_detection_controller.setShortcut('Ctrl+D')

        self.action_slice_meshes = QAction('&Slice meshes', parent)
        self.action_slice_meshes.setIcon(IconCollection.get('flash_on.svg'))
        self.action_slice_meshes.setShortcut('Ctrl+S')

        self.action_slice_blocks = QAction('Slice &blocks', parent)
        self.action_slice_blocks.setIcon(IconCollection.get('flash_on.svg'))
        self.action_slice_blocks.setShortcut('Ctrl+B')

        self.action_slice_points = QAction('Slice &points', parent)
        self.action_slice_points.setIcon(IconCollection.get('flash_on.svg'))
        self.action_slice_points.setShortcut('Ctrl+Shift+P')

        self.action_xsection = QAction('&Cross-section', parent)
        self.action_xsection.setIcon(IconCollection.get('flash_on.svg'))
        self.action_xsection.setShortcut('Ctrl+Shift+S')

        self.action_viewer_properties = QAction('&Viewer properties', parent)
        self.action_viewer_properties.setIcon(IconCollection.get('compact_camera.svg'))
        self.action_viewer_properties.setShortcut('Ctrl+C')

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

        self.action_perspective_projection = QAction('P&erspective projection', parent)
        self.action_perspective_projection.setIcon(IconCollection.get('ruler.svg'))
        self.action_perspective_projection.setShortcut('Ctrl+4')

        self.action_orthographic_projection = QAction('O&rthographic projection', parent)
        self.action_orthographic_projection.setIcon(IconCollection.get('ruler.svg'))
        self.action_orthographic_projection.setShortcut('Ctrl+5')

        self.action_take_screenshot = QAction('&Take screenshot', parent)
        self.action_take_screenshot.setIcon(IconCollection.get('webcam.svg'))
        self.action_take_screenshot.setShortcut('Shift+S')

        self.action_fix_wobbling = QAction('Fix &wobbling', parent)
        self.action_fix_wobbling.setIcon(IconCollection.get('services.svg'))
        self.action_fix_wobbling.setShortcut('Ctrl+K')
