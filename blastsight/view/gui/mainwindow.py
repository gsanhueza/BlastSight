#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
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

from .dialogs.helpdialog import HelpDialog
from .dialogs.aboutdialog import AboutDialog
from .iconcollection import IconCollection

from .tools import uic
from ..threadworker import ThreadWorker


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(f'{pathlib.Path(__file__).parent}/UI/mainwindow.ui', self)
        self.resize(1000, 620)

        self.setWindowTitle('BlastSight')
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

        self.settings = QSettings('BlastSight', application='blastsight', parent=self)

        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar(self.statusBar)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximumWidth(self.width() / 5)
        self.progress_bar.hide()
        self.statusBar.addPermanentWidget(self.progress_bar)

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
        if not actions.action_animate.isChecked():
            actions.action_animate.trigger()

        # Set camera widget as hidden
        self.dockWidget_camera.hide()

        # self.title = self.windowTitle()
        # self.viewer.signal_fps_updated.connect(lambda x: self.setWindowTitle(f'{self.title} (FPS: {x:.1f})'))

    def generate_menubar(self) -> None:
        actions = self.toolbar.action_collection

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

        self.menu_View.addAction(actions.action_camera_properties)
        self.menu_View.addAction(actions.action_plan_view)
        self.menu_View.addAction(actions.action_north_view)
        self.menu_View.addAction(actions.action_east_view)
        self.menu_View.addAction(actions.action_fit_to_screen)
        self.menu_View.addSeparator()
        self.menu_View.addAction(actions.action_autofit)
        self.menu_View.addAction(actions.action_animate)
        self.menu_View.addAction(actions.action_autorotate)
        self.menu_View.addAction(actions.action_turbo_rendering)
        self.menu_View.addSeparator()
        self.menu_View.addAction(actions.action_perspective_projection)
        self.menu_View.addAction(actions.action_orthographic_projection)
        self.menu_View.addSeparator()
        self.menu_View.addAction(actions.action_take_screenshot)

        self.menu_Tools.addAction(actions.action_slice_meshes)
        self.menu_Tools.addAction(actions.action_slice_blocks)
        self.menu_Tools.addAction(actions.action_detection_mode)
        self.menu_Tools.addAction(actions.action_measurement_mode)
        self.menu_Tools.addSeparator()
        self.menu_Tools.addAction(actions.action_normal_mode)
        self.menu_Tools.addAction(actions.action_cross_section)

        self.menu_Help.addAction(actions.action_help)
        self.menu_Help.addAction(actions.action_about)

    def connect_actions(self) -> None:
        actions = self.toolbar.action_collection

        # Toolbar/Tree/Camera
        self.toolbar.connect_viewer(self.viewer)
        self.toolbar.connect_tree(self.dockWidget_tree)
        self.toolbar.connect_camera(self.dockWidget_camera)
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
        actions.action_detection_mode.triggered.connect(self.slot_detection_mode)
        actions.action_measurement_mode.triggered.connect(self.slot_measurement_mode)

        actions.action_normal_mode.triggered.connect(self.slot_normal_mode)
        actions.action_cross_section.triggered.connect(self.slot_cross_section)

        # Help
        actions.action_help.triggered.connect(self.slot_help)
        actions.action_about.triggered.connect(self.slot_about)

        # Viewer signals
        self.viewer.signal_fps_updated.connect(self.print_fps)
        self.viewer.signal_mode_updated.connect(self.slot_mode_updated)
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

    def slot_mode_updated(self, mode: str) -> None:
        self.statusBar.showMessage(f'Mode: {mode}')

    def slot_mesh_distances(self, distance_dict: dict) -> None:
        self.statusBar.showMessage(f'Distance: {distance_dict.get("distance")}')

    def slot_elements_detected(self, attributes: list) -> None:
        id_list = sorted(map(lambda attr: attr.get('id', -1), attributes))
        self.statusBar.showMessage(f'Detected elements: {id_list}')

    """
    Slots for cross-sections
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
        def executer_standard(origin, normal) -> None:
            slices = self.viewer.slice_meshes(origin, normal)
            self.add_mesh_slices(slices)

        def executer_cross(origin, normal) -> None:
            self.viewer.cross_section(origin, normal)

        def handler(description: dict) -> None:
            if self.toolbar.action_collection.action_cross_section.isChecked():
                self.handle_slices(description, executer_cross)
            else:
                self.handle_slices(description, executer_standard)

            # Disconnect
            self.viewer.set_normal_mode()
            self.viewer.signal_slice_description.disconnect()

        self.viewer.set_slice_mode()
        self.viewer.signal_slice_description.connect(handler)

    def slot_slice_blocks(self) -> None:
        def executer(origin, normal) -> None:
            slices = self.viewer.slice_blocks(origin, normal)
            self.add_block_slices(slices)

        def handler(description: dict) -> None:
            self.handle_slices(description, executer)

            # Disconnect
            self.viewer.set_normal_mode()
            self.viewer.signal_slice_description.disconnect()

        self.viewer.set_slice_mode()
        self.viewer.signal_slice_description.connect(handler)

    def slot_cross_section(self, status: bool) -> None:
        self.viewer.set_cross_section(status)

        # Make all meshes either semi-transparent or fully opaque
        for drawable in self.viewer.get_all_drawables():
            drawable.alpha *= 0.1 if status else 10.0

        self.viewer.update_all()

    def add_mesh_slices(self, slice_list: list) -> None:
        def add_slice(description: dict) -> None:
            slices = description.get('vertices')
            mesh_id = description.get('element_id')
            mesh = self.viewer.get_drawable(mesh_id)

            def add_subslice(subslice, i: int) -> None:
                self.viewer.lines(vertices=subslice,
                                  color=mesh.color,
                                  name=f'MESHSLICE_{i}_{mesh.name}',
                                  extension='csv',
                                  loop=True)

            # Execute add_subslice for all subslices of the slice
            list(map(add_subslice, slices, range(len(slices))))

        # Execute add_slice over all slice descriptions
        list(map(add_slice, slice_list))

    def add_block_slices(self, slice_list: list) -> None:
        def add_slice(description: dict) -> None:
            indices = description.get('indices')
            block_id = description.get('element_id')
            block = self.viewer.get_drawable(block_id)

            if 'SLICE' in str(block.name):
                return

            self.viewer.blocks(vertices=block.vertices[indices],
                               values=block.values[indices],
                               color=block.color[indices],
                               vmin=block.vmin,
                               vmax=block.vmax,
                               colormap=block.colormap,
                               block_size=block.block_size,
                               name=f'BLOCKSLICE_{block.name}',
                               extension='csv')

        # Execute add_slice over all slice descriptions
        list(map(add_slice, slice_list))

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

        path_list = sorted([p for p in paths if p != ''])
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
    Slot for screenshots
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
        filters = 'BlastSight FIXME (*.h5m);;'

        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self,
            directory=proposed_path,
            filter=filters)

        # Execute method
        if bool(path):
            self.statusBar.showMessage('Exporting...')
            self._thread_runner(self.viewer.export_element, path, _id)

    """
    Slots for modifying interaction modes
    """
    def slot_normal_mode(self) -> None:
        self.viewer.set_normal_mode()

    def slot_detection_mode(self) -> None:
        self.viewer.set_detection_mode()

    def slot_measurement_mode(self) -> None:
        self.viewer.set_measurement_mode()

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
