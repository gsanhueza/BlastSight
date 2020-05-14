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

from .camerawidget import CameraWidget
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
        self.settings = QSettings('BlastSight', application='blastsight', parent=self)
        self.filters_dict = {
            'mesh': 'Mesh Files (*.dxf *.off *.h5m);;'
                    'DXF Files (*.dxf);;'
                    'OFF Files (*.off);;'
                    'H5M Files (*.h5m);;'
                    'All Files (*.*)',
            'block': 'Block Files (*.csv *.h5p *.out);;'
                     'CSV Files (*.csv);;'
                     'H5P Files (*.h5p);;'
                     'GSLib Files (*.out);;'
                     'All Files (*.*)',
            'point': 'Point Files (*.csv *.h5p *.out);;'
                     'CSV Files (*.csv);;'
                     'H5P Files (*.h5p);;'
                     'GSLib Files (*.out);;'
                     'All Files (*.*)',
            'line': 'Line Files (*.csv *.dxf);;'
                    'CSV Files (*.csv);;'
                    'DXF Files (*.csv);;'
                    'All Files (*.*)',
            'tube': 'Tube Files (*.csv *.dxf);;'
                    'CSV Files (*.csv);;'
                    'DXF Files (*.csv);;'
                    'All Files (*.*)',
        }

        # Extra actions
        actions = self.toolbar.action_collection
        self.toolbar.addAction(actions.action_quit)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.generate_menubar()
        self.connect_actions()

        # Set auto-fit as True when starting the app
        if not actions.action_autofit_to_screen.isChecked():
            actions.action_autofit_to_screen.trigger()

        # Set animated as True when starting the app
        if not actions.action_animated_viewer.isChecked():
            actions.action_animated_viewer.trigger()

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
        self.menu_View.addAction(actions.action_autofit_to_screen)
        self.menu_View.addAction(actions.action_animated_viewer)
        self.menu_View.addAction(actions.action_turbo_rendering)
        self.menu_View.addSeparator()
        self.menu_View.addAction(actions.action_perspective_projection)
        self.menu_View.addAction(actions.action_orthographic_projection)
        self.menu_View.addSeparator()
        self.menu_View.addAction(actions.action_take_screenshot)

        self.menu_Tools.addAction(actions.action_slice_mode)
        self.menu_Tools.addAction(actions.action_detection_mode)
        self.menu_Tools.addAction(actions.action_measurement_mode)
        self.menu_Tools.addSeparator()
        self.menu_Tools.addAction(actions.action_normal_mode)

        self.menu_Help.addAction(actions.action_help)
        self.menu_Help.addAction(actions.action_about)

    def connect_actions(self) -> None:
        actions = self.toolbar.action_collection

        # Toolbar/Tree
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
        # actions.action_camera_properties.triggered.connect(self.handle_camera)
        actions.action_take_screenshot.triggered.connect(self.handle_screenshot)

        # Tools
        actions.action_detection_mode.triggered.connect(self.slot_detection_mode)
        actions.action_slice_mode.triggered.connect(self.slot_slice_mode)
        actions.action_measurement_mode.triggered.connect(self.slot_measurement_mode)
        actions.action_normal_mode.triggered.connect(self.slot_normal_mode)

        # Help
        actions.action_help.triggered.connect(self.slot_help)
        actions.action_about.triggered.connect(self.slot_about)

        # Viewer signals
        self.viewer.signal_fps_updated.connect(self.print_fps)
        self.viewer.signal_mode_updated.connect(self.slot_mode_updated)
        self.viewer.signal_mesh_clicked.connect(self.slot_mesh_clicked)
        self.viewer.signal_mesh_distances.connect(self.slot_mesh_distances)
        self.viewer.signal_slice_description.connect(self.slot_slice_description)

        self.viewer.signal_load_success.connect(self.slot_element_load_success)
        self.viewer.signal_load_failure.connect(self.slot_element_load_failure)
        self.viewer.signal_export_success.connect(self.slot_element_export_success)
        self.viewer.signal_export_failure.connect(self.slot_element_export_failure)

        # TreeWidget actions
        self.treeWidget.signal_export_mesh.connect(self.dialog_export_mesh)
        self.treeWidget.signal_export_blocks.connect(self.dialog_export_blocks)
        self.treeWidget.signal_export_points.connect(self.dialog_export_points)
        self.treeWidget.signal_export_lines.connect(self.dialog_export_lines)
        self.treeWidget.signal_export_tubes.connect(self.dialog_export_tubes)

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
        self.viewer.update_turbo()
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

    def slot_mesh_clicked(self, mesh_attributes: list) -> None:
        id_list = [attr.get('id', -1) for attr in mesh_attributes]
        self.statusBar.showMessage(f'Detected meshes: {id_list}')

    def slot_slice_description(self, description: dict) -> None:
        origin = description.get('origin')
        normal = description.get('normal')
        up = description.get('up')

        # Slice elements
        mesh_slices = self.viewer.slice_meshes(origin, normal)
        block_slices = self.viewer.slice_blocks(origin, normal)

        # Add to elements
        self.add_mesh_slices(mesh_slices)
        self.add_block_slices(block_slices)

        # Auto-rotate camera to meet cross-section
        self.viewer.set_camera_from_vectors(normal, up)

        # Auto-exit slice mode
        self.viewer.set_normal_mode()

    def add_mesh_slices(self, slice_list: list) -> None:
        for sliced_meshes in slice_list:
            slices = sliced_meshes.get('vertices')
            mesh_id = sliced_meshes.get('element_id')
            mesh = self.viewer.get_drawable(mesh_id)

            if 'SLICE' in str(mesh.name):
                continue

            for i, vert_slice in enumerate(slices):
                self.viewer.lines(vertices=vert_slice,
                                  color=mesh.color,
                                  name=f'MESHSLICE_{i}_{mesh.name}',
                                  extension='csv',
                                  loop=True)

    def add_block_slices(self, slice_list: list) -> None:
        for sliced_blocks in slice_list:
            indices = sliced_blocks.get('indices')
            block_id = sliced_blocks.get('element_id')
            block = self.viewer.get_drawable(block_id)

            if 'SLICE' in str(block.name):
                continue

            self.viewer.blocks(vertices=block.vertices[indices],
                               values=block.values[indices],
                               color=block.color[indices],
                               vmin=block.vmin,
                               vmax=block.vmax,
                               colormap=block.colormap,
                               block_size=block.block_size,
                               name=f'BLOCKSLICE_{block.name}',
                               extension='csv')

    """
    Common functionality for loading/exporting
    """
    def _threaded_load(self, method: classmethod, *args, **kwargs) -> None:
        self.statusBar.showMessage('Loading...')

        worker = ThreadWorker(method, *args, **kwargs)
        QThreadPool.globalInstance().start(worker)

    def _threaded_export(self, method: classmethod, path: str, _id: int) -> None:
        self.statusBar.showMessage('Exporting...')

        worker = ThreadWorker(method, path, _id)
        QThreadPool.globalInstance().start(worker)

    def _dialog_load_element(self, loader: classmethod, hint: str, *args, **kwargs) -> None:
        (paths, selected_filter) = QFileDialog.getOpenFileNames(
            parent=self,
            directory=self.last_dir,
            filter=self.filters_dict.get(hint))

        for path in sorted([p for p in paths if p != '']):
            self._threaded_load(loader, path, *args, **kwargs)
            self.last_dir = QFileInfo(path).absoluteDir().absolutePath()

    def _dialog_load_folder(self, loader: classmethod, *args, **kwargs) -> None:
        path = QFileDialog.getExistingDirectory(
            parent=self,
            directory=self.last_dir,
            options=QFileDialog.ShowDirsOnly)

        # Execute method
        if bool(path):
            self._threaded_load(loader, path, *args, **kwargs)
            self.last_dir = path

    def _dialog_export_element(self, _id: int, filters: str, method: classmethod) -> None:
        proposed_path = QDir(self.last_dir).filePath(self.viewer.get_drawable(_id).element.name)

        (path, selected_filter) = QFileDialog.getSaveFileName(
            parent=self,
            directory=proposed_path,
            filter=filters)

        if path != '':
            # Execute method
            self._threaded_export(method, path, _id)

    """
    Slots for pop-up dialogs
    """
    def handle_camera(self) -> None:
        camera = CameraWidget()
        camera.setWindowIcon(self.windowIcon())
        camera.connect_viewer(self.viewer)

        camera.show()

    def handle_screenshot(self) -> None:
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
    Slots for exporting files
    """
    def dialog_export_mesh(self, _id: int) -> None:
        self._dialog_export_element(_id=_id,
                                    filters='BlastSight mesh (*.h5m);;',
                                    method=self.viewer.export_mesh)

    def dialog_export_blocks(self, _id: int) -> None:
        self._dialog_export_element(_id=_id,
                                    filters='BlastSight blocks (*.h5p);;',
                                    method=self.viewer.export_blocks)

    def dialog_export_points(self, _id: int) -> None:
        self._dialog_export_element(_id=_id,
                                    filters='BlastSight points (*.h5p);;',
                                    method=self.viewer.export_points)

    def dialog_export_lines(self, _id: int) -> None:
        self._dialog_export_element(_id=_id,
                                    filters='BlastSight lines (*.csv);;',
                                    method=self.viewer.export_lines)

    def dialog_export_tubes(self, _id: int) -> None:
        self._dialog_export_element(_id=_id,
                                    filters='BlastSight tubes (*.csv);;',
                                    method=self.viewer.export_tubes)

    """
    Slots for modifying controller modes
    """
    def slot_normal_mode(self) -> None:
        self.viewer.set_normal_mode()

    def slot_detection_mode(self) -> None:
        self.viewer.set_detection_mode()

    def slot_slice_mode(self) -> None:
        self.viewer.set_slice_mode()

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
