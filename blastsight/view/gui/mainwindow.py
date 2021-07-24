#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from datetime import datetime
from qtpy.QtCore import QDir
from qtpy.QtCore import Qt
from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QSettings
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QProgressBar

from .dialogs.aboutdialog import AboutDialog
from .dialogs.helpdialog import HelpDialog
from .iconcollection import IconCollection
from .gridwidget import GridWidget
from .xsectionwidget import XSectionWidget

from .tools import uic
from ..threadworker import ThreadWorker


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/mainwindow.ui', self)

        self.setWindowTitle('BlastSightDM')
        self.setWindowIcon(IconCollection.get('blastsight.png'))
        self.toolbar.setWindowTitle('Toolbar')

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)
        self.statusBar.showMessage('Ready')

        # Attributes
        self.filters_dict = {
            'mesh': {
                'load': 'Mesh Files (*.dxf *.off *.h5m);;'
                        'DXF Files (*.dxf);;'
                        'OFF Files (*.off);;'
                        'H5M Files (*.h5m);;'
                        'All Files (*.*)',
                'export': 'BlastSight Mesh (*.h5m);;'
                          'OFF File (*.off);;'
            },
            'block': {
                'load': 'Block Files (*.csv *.h5p *.out);;'
                        'CSV Files (*.csv);;'
                        'H5P Files (*.h5p);;'
                        'GSLib Files (*.out);;'
                        'All Files (*.*)',
                'export': 'BlastSight Blocks (*.h5p);;'
                          'CSV File (*.csv);;'
            },
            'point': {
                'load': 'Point Files (*.csv *.h5p *.out);;'
                        'CSV Files (*.csv);;'
                        'H5P Files (*.h5p);;'
                        'GSLib Files (*.out);;'
                        'All Files (*.*)',
                'export': 'BlastSight Points (*.h5p);;'
                          'CSV File (*.csv);;'
            },
            'line': {
                'load': 'Line Files (*.csv *.dxf);;'
                        'CSV Files (*.csv);;'
                        'DXF Files (*.dxf);;'
                        'All Files (*.*)',
                'export': 'CSV File (*.csv);;'
            },
            'tube': {
                'load': 'Line Files (*.csv *.dxf);;'
                        'CSV Files (*.csv);;'
                        'DXF Files (*.dxf);;'
                        'All Files (*.*)',
                'export': 'CSV File (*.csv);;'
            }
        }

        self.settings = QSettings('BlastSightDM', application='blastsight-dm', parent=self)

        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar(self.statusBar)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximumWidth(self.width() / 5)
        self.progress_bar.hide()
        self.statusBar.addPermanentWidget(self.progress_bar)

        # Grid Widget
        self.grid_widget = GridWidget()
        self.grid_widget.connect_viewer(self.viewer)

        # XSection Widget
        self.xsection_widget = XSectionWidget()
        self.xsection_widget.connect_viewer(self.viewer)

        # Extra actions
        actions = self.toolbar.action_collection
        self.toolbar.addAction(actions.action_quit)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.generate_menubar()
        self.connect_actions()

        # Set auto-fit as True when starting the app
        if not actions.action_autofit.isChecked():
            actions.action_autofit.trigger()

        # Set auto-rotate as True when starting the app
        if not actions.action_autorotate.isChecked():
            actions.action_autorotate.trigger()

        # Set animated as True when starting the app
        if not actions.action_animated.isChecked():
            actions.action_animated.trigger()

        # Set camera widget as hidden
        self.dockWidget_camera.hide()

    def generate_menubar(self) -> None:
        actions = self.toolbar.action_collection

        # File
        self.menu_File.addAction(actions.action_load_mesh)
        self.menu_File.addAction(actions.action_load_blocks)
        self.menu_File.addAction(actions.action_load_points)
        self.menu_File.addAction(actions.action_load_lines)
        self.menu_File.addAction(actions.action_load_tubes)
        self.menu_File.addSeparator()
        self.menu_File.addAction(actions.action_load_mesh_folder)
        self.menu_File.addAction(actions.action_load_blocks_folder)
        self.menu_File.addAction(actions.action_load_points_folder)
        self.menu_File.addAction(actions.action_load_lines_folder)
        self.menu_File.addAction(actions.action_load_tubes_folder)
        self.menu_File.addSeparator()
        self.menu_File.addAction(actions.action_quit)

        # View
        self.menu_View.addAction(actions.action_viewer_properties)
        self.menu_View.addAction(actions.action_plan_view)
        self.menu_View.addAction(actions.action_north_view)
        self.menu_View.addAction(actions.action_east_view)
        self.menu_View.addAction(actions.action_fit_to_screen)
        self.menu_View.addSeparator()
        self.menu_View.addAction(actions.action_perspective_projection)
        self.menu_View.addAction(actions.action_orthographic_projection)
        self.menu_View.addSeparator()
        self.menu_View.addAction(actions.action_grid)
        self.menu_View.addAction(actions.action_take_screenshot)

        # Tools
        self.menu_Tools.addAction(actions.action_slice_meshes)
        self.menu_Tools.addAction(actions.action_slice_blocks)
        self.menu_Tools.addAction(actions.action_slice_points)
        self.menu_Tools.addAction(actions.action_detection_controller)
        self.menu_Tools.addAction(actions.action_measurement_controller)
        self.menu_Tools.addSeparator()
        self.menu_Tools.addAction(actions.action_xsection)
        self.menu_Tools.addAction(actions.action_normal_controller)

        # Settings
        self.menu_Settings.addAction(actions.action_autofit)
        self.menu_Settings.addAction(actions.action_animated)
        self.menu_Settings.addAction(actions.action_autorotate)
        self.menu_Settings.addAction(actions.action_turbo_rendering)

        # Help
        self.menu_Help.addAction(actions.action_help)
        self.menu_Help.addAction(actions.action_about)

    def connect_actions(self) -> None:
        actions = self.toolbar.action_collection

        # Toolbar/Tree/Camera
        self.toolbar.connect_viewer(self.viewer)
        self.toolbar.connect_tree(self.dockWidget_tree)
        self.toolbar.connect_camera(self.dockWidget_camera)
        self.toolbar.connect_xsection(self.xsection_widget)
        self.toolbar.connect_grid(self.grid_widget)

        self.cameraWidget.connect_viewer(self.viewer)
        self.treeWidget.connect_viewer(self.viewer)
        self.treeWidget.enable_exportability(True)

        # File
        actions.action_load_mesh.triggered.connect(self.dialog_load_mesh)
        actions.action_load_blocks.triggered.connect(self.dialog_load_blocks)
        actions.action_load_points.triggered.connect(self.dialog_load_points)
        actions.action_load_lines.triggered.connect(self.dialog_load_lines)
        actions.action_load_tubes.triggered.connect(self.dialog_load_tubes)

        actions.action_load_mesh_folder.triggered.connect(self.dialog_load_mesh_folder)
        actions.action_load_blocks_folder.triggered.connect(self.dialog_load_blocks_folder)
        actions.action_load_points_folder.triggered.connect(self.dialog_load_points_folder)
        actions.action_load_lines_folder.triggered.connect(self.dialog_load_lines_folder)
        actions.action_load_tubes_folder.triggered.connect(self.dialog_load_tubes_folder)

        actions.action_quit.triggered.connect(self.close)

        # View
        actions.action_take_screenshot.triggered.connect(self.slot_screenshot)

        # Tools
        actions.action_slice_meshes.triggered.connect(self.slot_slice_meshes)
        actions.action_slice_blocks.triggered.connect(self.slot_slice_blocks)
        actions.action_slice_points.triggered.connect(self.slot_slice_points)
        actions.action_detection_controller.triggered.connect(self.slot_detection_controller)
        actions.action_measurement_controller.triggered.connect(self.slot_measurement_controller)

        actions.action_normal_controller.triggered.connect(self.slot_normal_controller)

        # Help
        actions.action_help.triggered.connect(self.slot_help)
        actions.action_about.triggered.connect(self.slot_about)

        # Viewer signals
        self.viewer.signal_fps_updated.connect(self.print_fps)
        self.viewer.signal_controller_updated.connect(self.slot_controller_updated)
        self.viewer.signal_elements_detected.connect(self.slot_elements_detected)
        self.viewer.signal_mesh_distances.connect(self.slot_mesh_distances)

        self.viewer.signal_load_success.connect(self.slot_element_load_success)
        self.viewer.signal_load_failure.connect(self.slot_element_load_failure)
        self.viewer.signal_export_success.connect(self.slot_element_export_success)
        self.viewer.signal_export_failure.connect(self.slot_element_export_failure)

        self.viewer.signal_process_updated.connect(self.slot_process_updated)
        self.viewer.signal_process_started.connect(self.slot_process_started)
        self.viewer.signal_process_finished.connect(self.slot_process_finished)

        # TreeWidget actions
        self.treeWidget.signal_export_element.connect(self._dialog_export_element)

    @property
    def last_dir(self) -> str:
        return self.settings.value('last_directory', '.')

    @last_dir.setter
    def last_dir(self, _last_dir: str) -> None:
        self.settings.setValue('last_directory', _last_dir)

    @staticmethod
    def print_fps(fps) -> None:
        print(f'               \r', end='')
        print(f'FPS: {fps:.1f} \r', end='')

    """
    Status bar updates
    """
    def slot_element_load_success(self, _id: int) -> None:
        self.statusBar.showMessage(f'Load successful (id: {_id}).')

    def slot_element_load_failure(self) -> None:
        self.statusBar.showMessage(f'Failed to load.')

    def slot_element_export_success(self, _id: int) -> None:
        self.statusBar.showMessage(f'Export successful (id: {_id}).')

    def slot_element_export_failure(self) -> None:
        self.statusBar.showMessage(f'Failed to export.')

    def slot_controller_updated(self, name: str) -> None:
        self.statusBar.showMessage(f'Controller: {name}')

    def slot_mesh_distances(self, distance_dict: dict) -> None:
        self.statusBar.showMessage(f'Distance: {distance_dict.get("distance")}')

    def slot_elements_detected(self, attributes: list) -> None:
        id_list = sorted(map(lambda attr: attr.get('id', -1), attributes))
        self.statusBar.showMessage(f'Detected elements: {id_list}')

    """
    Slots for slices
    """
    def handle_slices(self, description: dict, executer: callable) -> None:
        # Retrieve description vectors
        origin = description.get('origin')
        normal = description.get('normal')
        up = description.get('up')

        # Execute the callable over the elements
        executer(origin, normal)

        # Auto-rotate camera to meet cross-section
        actions = self.toolbar.action_collection
        if actions.action_autorotate.isChecked():
            self.viewer.set_camera_from_vectors(normal, up)

    def slot_slice_meshes(self) -> None:
        def executer(origin, normal) -> None:
            slices = self.viewer.slice_meshes(origin, normal)
            self.add_mesh_slices(slices)

        def handler(description: dict) -> None:
            self.handle_slices(description, executer)

            # Disconnect
            self.viewer.set_normal_controller()
            self.viewer.signal_slice_description.disconnect()

        self.viewer.set_slice_controller()
        self.viewer.signal_slice_description.connect(handler)

    def slot_slice_blocks(self) -> None:
        def executer(origin, normal) -> None:
            slices = self.viewer.slice_blocks(origin, normal)
            self.add_block_slices(slices)

        def handler(description: dict) -> None:
            self.handle_slices(description, executer)

            # Disconnect
            self.viewer.set_normal_controller()
            self.viewer.signal_slice_description.disconnect()

        self.viewer.set_slice_controller()
        self.viewer.signal_slice_description.connect(handler)

    def slot_slice_points(self) -> None:
        def executer(origin, normal) -> None:
            slices = self.viewer.slice_points(origin, normal)
            self.add_point_slices(slices)

        def handler(description: dict) -> None:
            self.handle_slices(description, executer)

            # Disconnect
            self.viewer.set_normal_controller()
            self.viewer.signal_slice_description.disconnect()

        self.viewer.set_slice_controller()
        self.viewer.signal_slice_description.connect(handler)

    def add_mesh_slices(self, slice_list: list) -> None:
        def add_slice(description: dict) -> None:
            slices = description.get('vertices')
            mesh_id = description.get('element_id')
            mesh = self.viewer.get_drawable(mesh_id)

            def add_subslice(subslice, num: int) -> None:
                self.viewer.lines(vertices=subslice,
                                  color=mesh.color,
                                  name=f'MESHSLICE_{num}_{mesh.name}',
                                  extension='csv',
                                  loop=True)

            # Execute add_subslice for all subslices of the slice
            for i, ssl in enumerate(slices):
                add_subslice(ssl, i)

        # Execute add_slice over all slice descriptions
        for sl in slice_list:
            add_slice(sl)

    def add_block_slices(self, slice_list: list) -> None:
        def add_slice(description: dict) -> None:
            indices = description.get('indices')
            block_id = description.get('element_id')
            block = self.viewer.get_drawable(block_id)

            if block.is_slice:
                return

            self.viewer.blocks(vertices=block.vertices[indices],
                               values=block.values[indices],
                               color=block.color[indices],
                               vmin=block.vmin,
                               vmax=block.vmax,
                               colormap=block.colormap,
                               block_size=block.block_size,
                               name=f'BLOCKSLICE_{block.name}',
                               extension='csv',
                               is_slice=True)

        # Execute add_slice over all slice descriptions
        for sl in slice_list:
            add_slice(sl)

    def add_point_slices(self, slice_list: list) -> None:
        def add_slice(description: dict) -> None:
            indices = description.get('indices')
            point_id = description.get('element_id')
            point = self.viewer.get_drawable(point_id)

            if point.is_slice:
                return

            self.viewer.points(vertices=point.vertices[indices],
                               values=point.values[indices],
                               color=point.color[indices],
                               vmin=point.vmin,
                               vmax=point.vmax,
                               colormap=point.colormap,
                               point_size=point.point_size,
                               name=f'POINTSLICE_{point.name}',
                               extension='csv',
                               is_slice=True)

        # Execute add_slice over all slice descriptions
        for sl in slice_list:
            add_slice(sl)

    """
    Common functionality for loading
    """
    @staticmethod
    def _thread_runner(method: callable, *args, **kwargs) -> None:
        worker = ThreadWorker(method, *args, **kwargs)
        QThreadPool.globalInstance().start(worker)

    def _dialog_load_element(self, loader: classmethod, hint: str, *args, **kwargs) -> None:
        (paths, selected_filter) = QFileDialog.getOpenFileNames(
            parent=self,
            directory=self.last_dir,
            filter=self.filters_dict.get(hint).get('load'))

        # If path == '', then bool(path) is False
        path_list = sorted(filter(bool, paths))

        if len(path_list) > 0:
            self.statusBar.showMessage(f'Loading {len(path_list)} element(s)...')
            self._thread_runner(self.viewer.load_multiple, path_list, loader, *args, **kwargs)
            self.last_dir = QFileInfo(path_list[-1]).absoluteDir().absolutePath()

    def _dialog_load_folder(self, loader: classmethod, *args, **kwargs) -> None:
        path = QFileDialog.getExistingDirectory(
            parent=self,
            directory=self.last_dir,
            options=QFileDialog.ShowDirsOnly)

        # Execute method
        if bool(path):
            self.statusBar.showMessage('Loading folder...')
            self._thread_runner(loader, path, *args, **kwargs)
            self.last_dir = path

    """
    Slots for progress updates
    """
    def slot_process_updated(self, value: int) -> None:
        self.progress_bar.setValue(value)

    def slot_process_started(self) -> None:
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def slot_process_finished(self,) -> None:
        self.progress_bar.hide()

    """
    Slot for extra items in view
    """
    def slot_screenshot(self) -> None:
        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self.viewer,
            directory=f'BlastSight Screenshot ({datetime.now().strftime("%Y%m%d-%H%M%S")})',
            filter='PNG image (*.png);;')

        self.viewer.take_screenshot(path)

    """
    Slots for loading files
    """
    def dialog_load_mesh(self) -> None:
        self._dialog_load_element(loader=self.viewer.load_mesh, hint='mesh')

    def dialog_load_blocks(self) -> None:
        self._dialog_load_element(loader=self.viewer.load_blocks, hint='block')

    def dialog_load_points(self) -> None:
        self._dialog_load_element(loader=self.viewer.load_points, hint='point')

    def dialog_load_lines(self) -> None:
        self._dialog_load_element(loader=self.viewer.load_lines, hint='line')

    def dialog_load_tubes(self) -> None:
        self._dialog_load_element(loader=self.viewer.load_tubes, hint='tube')

    def dialog_load_mesh_folder(self) -> None:
        self._dialog_load_folder(loader=self.viewer.load_mesh_folder)

    def dialog_load_blocks_folder(self) -> None:
        self._dialog_load_folder(loader=self.viewer.load_blocks_folder)

    def dialog_load_points_folder(self) -> None:
        self._dialog_load_folder(loader=self.viewer.load_points_folder)

    def dialog_load_lines_folder(self) -> None:
        self._dialog_load_folder(loader=self.viewer.load_lines_folder)

    def dialog_load_tubes_folder(self) -> None:
        self._dialog_load_folder(loader=self.viewer.load_tubes_folder)

    """
    Slots for exporting elements
    """
    def _dialog_export_element(self, _id: int) -> None:
        element = self.viewer.get_drawable(_id).element
        proposed_path = QDir(self.last_dir).filePath(element.name)

        # TODO Check hints by element type
        filters = 'BlastSight Mesh (*.h5m);;'\
                  'BlastSight Blocks/Points (*.h5p);;'

        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self,
            directory=proposed_path,
            filter=filters)

        # Execute method
        if bool(path):
            self.statusBar.showMessage('Exporting...')
            self._thread_runner(self.viewer.export_element, path, _id)

    """
    Slots for modifying interaction controllers
    """
    def slot_normal_controller(self) -> None:
        self.viewer.set_normal_controller()

    def slot_detection_controller(self) -> None:
        self.viewer.set_detection_controller()

    def slot_measurement_controller(self) -> None:
        self.viewer.set_measurement_controller()

    """
    Slots for showing help/about dialogs
    """
    def slot_help(self) -> None:
        HelpDialog(self).exec_()

    def slot_about(self) -> None:
        AboutDialog(self).exec_()

    """
    Events pass-through
    """
    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dragEnterEvent(event, *args, **kwargs)

    def dropEvent(self, event, *args, **kwargs) -> None:
        self.viewer.dropEvent(event, *args, **kwargs)
