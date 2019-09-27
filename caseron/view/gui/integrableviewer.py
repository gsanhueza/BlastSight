#!/usr/bin/env python

import numpy as np
import traceback

from OpenGL.GL import *

from qtpy.QtCore import QPoint
from qtpy.QtCore import Signal
from qtpy.QtCore import QDirIterator
from qtpy.QtCore import QFileInfo
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QPixmap
from qtpy.QtGui import QRegion
from qtpy.QtGui import QVector3D
from qtpy.QtGui import QVector4D
from qtpy.QtWidgets import QOpenGLWidget

from ..drawables.glconstantcollection import GLConstantCollection
from ..drawables.gldrawablecollection import GLDrawableCollection

from ..drawables.axisgl import AxisGL
from ..drawables.backgroundgl import BackgroundGL
from ..drawables.blockgl import BlockGL
from ..drawables.linegl import LineGL
from ..drawables.meshgl import MeshGL
from ..drawables.pointgl import PointGL
from ..drawables.tubegl import TubeGL

from ..fpscounter import FPSCounter

from ...controller.detectionmode import DetectionMode
from ...controller.normalmode import NormalMode
from ...controller.slicemode import SliceMode
from ...controller.measurementmode import MeasurementMode

from ...model import utils
from ...model.model import Model
from ...model.elements.nullelement import NullElement


class IntegrableViewer(QOpenGLWidget):
    # Signals
    signal_file_modified = Signal()
    signal_fps_updated = Signal(float)
    signal_mesh_clicked = Signal(object)
    signal_mesh_distances = Signal(object)
    signal_mode_updated = Signal(str)

    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        # Model
        self._model = Model()

        # Controller mode
        self.signal_mode_updated.connect(lambda m: print(f'MODE: {m}'))
        self.current_mode = None
        self.set_normal_mode()

        # Drawable elements
        self.constant_collection = GLConstantCollection(self)
        self.drawable_collection = GLDrawableCollection(self)

        self.constant_collection.add(BackgroundGL(NullElement(id='BG')))
        self.constant_collection.add(AxisGL(NullElement(id='AXIS')))

        # Camera/World/Projection
        self._camera = QMatrix4x4()
        self._world = QMatrix4x4()
        self._proj = QMatrix4x4()

        # Initial positions and rotations
        self.rotation_center = [0.0, 0.0, 0.0]
        self.rotation_angle = [0.0, 0.0, 0.0]
        self.camera_position = [0.0, 0.0, 200.0]

        # FPS Counter
        self.fps_counter = FPSCounter()
        self.signal_fps_updated.connect(self.print_fps)

        # Extra information
        self.fov = 45.0
        self.projection_mode = 'perspective'
        # self.projection_mode = 'orthographic'

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, _model):
        self._model = _model

    @property
    def camera(self):
        return self._camera

    @property
    def world(self):
        return self._world

    @property
    def proj(self):
        return self._proj

    @property
    def last_id(self) -> int:
        return self.drawable_collection.last_id

    @property
    def camera_position(self) -> np.ndarray:
        return np.array([self.xCameraPos, self.yCameraPos, self.zCameraPos])

    @property
    def rotation_angle(self) -> np.ndarray:
        return np.array([self.xCenterRot, self.yCenterRot, self.zCenterRot])

    @property
    def rotation_center(self) -> np.ndarray:
        return np.array([self.xCenterPos, self.yCenterPos, self.zCenterPos])

    @camera_position.setter
    def camera_position(self, pos: list) -> None:
        self.xCameraPos, self.yCameraPos, self.zCameraPos = pos

    @rotation_angle.setter
    def rotation_angle(self, rot: list) -> None:
        self.xCenterRot, self.yCenterRot, self.zCenterRot = rot

    @rotation_center.setter
    def rotation_center(self, _center: list) -> None:
        self.xCenterPos, self.yCenterPos, self.zCenterPos = _center

    """
    Load methods
    """
    def add_drawable(self, method: classmethod, drawable_type: type, *args, **kwargs):
        try:
            element = method(*args, **kwargs)
            drawable = drawable_type(element, *args, **kwargs)
            self.drawable_collection.add(drawable)

            self.signal_file_modified.emit()
            self.update()

            return drawable
        except Exception:
            traceback.print_exc()
            return None

    def mesh(self, *args, **kwargs) -> MeshGL:
        return self.add_drawable(self.model.mesh, MeshGL, *args, **kwargs)

    def blocks(self, *args, **kwargs) -> BlockGL:
        return self.add_drawable(self.model.blocks, BlockGL, *args, **kwargs)

    def points(self, *args, **kwargs) -> PointGL:
        return self.add_drawable(self.model.points, PointGL, *args, **kwargs)

    def lines(self, *args, **kwargs) -> LineGL:
        return self.add_drawable(self.model.lines, LineGL, *args, **kwargs)

    def tubes(self, *args, **kwargs) -> TubeGL:
        return self.add_drawable(self.model.tubes, TubeGL, *args, **kwargs)

    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshGL:
        return self.add_drawable(self.model.mesh_by_path, MeshGL, path, *args, **kwargs)

    def blocks_by_path(self, path: str, *args, **kwargs) -> BlockGL:
        return self.add_drawable(self.model.blocks_by_path, BlockGL, path, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointGL:
        return self.add_drawable(self.model.points_by_path, PointGL, path, *args, **kwargs)

    """
    Export methods
    """
    def export_mesh(self, path, _id):
        self.model.export_mesh(path, _id)

    def export_blocks(self, path, _id):
        self.model.export_blocks(path, _id)

    def export_points(self, path, _id):
        self.model.export_points(path, _id)

    """
    Individual drawable manipulation
    """
    def show_drawable(self, _id: int) -> None:
        self.get_drawable(_id).show()
        self.update()

    def hide_drawable(self, _id: int) -> None:
        self.get_drawable(_id).hide()
        self.update()

    def get_drawable(self, _id: int):
        return self.drawable_collection[_id]

    def update_drawable(self, _id: int) -> None:
        self.makeCurrent()
        self.get_drawable(_id).setup_attributes()
        self.update()

    def delete(self, _id: int) -> None:
        self.makeCurrent()
        self.model.delete(_id)
        self.drawable_collection.delete(_id)
        self.signal_file_modified.emit()
        self.update()

    def clear(self) -> None:
        for _id in list(self.drawable_collection.keys()):
            self.delete(_id)

    def camera_at(self, _id: int) -> None:
        self.fit_boundaries_to_screen(*self.get_drawable(_id).element.bounding_box)
        self.update()

    def plan_view(self) -> None:
        self.xCenterRot, self.yCenterRot, self.zCenterRot = [0.0, 0.0, 0.0]
        self.update()

    def north_view(self) -> None:
        self.xCenterRot, self.yCenterRot, self.zCenterRot = [270.0, 0.0, 270.0]
        self.update()

    def east_view(self) -> None:
        self.xCenterRot, self.yCenterRot, self.zCenterRot = [270.0, 0.0, 0.0]
        self.update()

    def fit_boundaries_to_screen(self, min_bound: np.ndarray, max_bound: np.ndarray) -> None:
        center = (min_bound + max_bound) / 2
        self.rotation_center = center
        self.camera_position = center

        # Put the camera in a position that allow us to see the element
        # A long trigonometric calculation got us this result.
        md = np.max(np.diff([min_bound, max_bound], axis=0))
        aspect = self.width() / self.height()
        fov_rad = self.fov * np.pi / 180.0

        if self.projection_mode == 'orthographic':
            fov_rad = np.pi / 2.0

        dist = (md / np.tan(fov_rad / 2) + md) / 2.0

        self.zCameraPos += 1.1 * dist / max(min(1.0, aspect), 1e-12)
        self.update()

    def fit_to_screen(self) -> None:
        drawables = [d for d in self.drawable_collection.values() if d.is_visible]

        if len(drawables) == 0:
            return

        min_all = np.inf * np.ones(3)
        max_all = -np.inf * np.ones(3)

        for drawable in drawables:
            min_bound, max_bound = drawable.element.bounding_box
            min_all = np.min((min_all, min_bound), axis=0)
            max_all = np.max((max_all, max_bound), axis=0)

        self.fit_boundaries_to_screen(min_all, max_all)
        self.update()

    """
    Internal methods
    """
    def initializeGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_POINT_SPRITE)
        glDisable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self) -> None:
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.world.setToIdentity()
        self.camera.setToIdentity()
        self.proj.setToIdentity()

        # Translate by rotation center (world position)
        self.world.translate(*self.rotation_center)

        # Allow rotation of the world
        self.world.rotate(self.xCenterRot, 1.0, 0.0, 0.0)
        self.world.rotate(self.yCenterRot, 0.0, 1.0, 0.0)
        self.world.rotate(self.zCenterRot, 0.0, 0.0, 1.0)

        # Restore world
        self.world.translate(*-self.rotation_center)

        # Translate the camera
        self.camera.translate(*-self.camera_position)

        # Project (Perspective/Orthographic)
        self.resizeGL(self.width(), self.height())

        # Draw every GLDrawable (meshes, block models, etc)
        glEnable(GL_BLEND)
        self.constant_collection.draw(self.proj, self.camera, self.world)
        self.drawable_collection.draw(self.proj, self.camera, self.world)

        # QPainter can draw *after* OpenGL finishes
        self.current_mode.overpaint(self)

        self.fps_counter.tick()
        self.signal_fps_updated.emit(self.fps_counter.fps)

    def resizeGL(self, w: float, h: float) -> None:
        if self.projection_mode == 'perspective':
            self.proj.perspective(self.fov, (w / h), 1.0, 10000.0)
        elif self.projection_mode == 'orthographic':
            z = max(self.zCameraPos - self.zCenterPos, 0.0)
            aspect = w / h
            self.proj.ortho(-z, z, -z / aspect, z / aspect, 0.0, 10000.0)

    """
    Utilities
    """
    @staticmethod
    def print_fps(fps) -> None:
        print(f'               \r', end='')
        print(f'FPS: {fps:.1f} \r', end='')

    def get_pixmap(self) -> QPixmap:
        pixmap = QPixmap(self.size())
        self.render(pixmap, QPoint(), QRegion(self.rect()))
        return pixmap

    def take_screenshot(self, save_path=None) -> None:
        if save_path is not None:
            self.get_pixmap().save(save_path)

    def pixel_to_clip(self, _x, _y, _z):
        # Click at bottom-left of screen => (-1.0, -1.0)
        # Click at top-right of screen => (1.0, 1.0)
        x = (2.0 * _x / self.width()) - 1.0
        y = 1.0 - (2.0 * _y / self.height())
        z = 1.0
        return x, y, z

    def unproject(self, _x, _y, _z, model, view, proj) -> QVector3D:
        # Adapted from http://antongerdelan.net/opengl/raycasting.html
        x, y, z = self.pixel_to_clip(_x, _y, _z)

        ray_eye = proj.inverted()[0] * QVector4D(x, y, -1.0, 1.0)
        ray_eye = QVector4D(ray_eye.x(), ray_eye.y(), -1.0, 0.0)

        ray_world = ((view * model).inverted()[0] * ray_eye).toVector3D()
        return ray_world.normalized()

    def ray_from_click(self, x: float, y: float, z: float) -> tuple:
        # Generates a ray from a click on screen
        # Assume perspective first
        ray = self.unproject(x, y, z, self.world, self.camera, self.proj)
        origin = (self.camera * self.world).inverted()[0].column(3).toVector3D()

        if self.projection_mode == 'orthographic':
            ray = self.unproject(self.width() / 2, self.height() / 2, z,
                                 self.world, self.camera, self.proj)

            # FIXME This only works when the world is not rotated
            aspect = self.width() / self.height()
            off_x, off_y, off_z = origin.z() * np.array([*self.pixel_to_clip(x, y, z)])
            offs = np.array([off_x, off_y / aspect, 0.0])

            # Hack to get the origin when the click is not exactly at center of screen
            self.camera.translate(*-offs)
            origin = (self.camera * self.world).inverted()[0].column(3).toVector3D()
            self.camera.translate(*offs)

        # To Numpy array
        ray = np.array([ray.x(), ray.y(), ray.z()])
        origin = np.array([origin.x(), origin.y(), origin.z()])

        return ray, origin

    def slice_from_rays(self, origin_list: list, ray_list: list) -> None:
        mesh_drawables = [m for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        mesh_elements = [m.element for m in mesh_drawables if 'SLICE' not in m.element.name]

        block_drawables = [m for m in self.drawable_collection.filter(BlockGL) if m.is_visible]
        block_elements = [m.element for m in block_drawables if 'SLICE' not in m.element.name]

        # A plane is created from `origin` and `ray_list`.
        # In perspective projection, the origin is the same.
        origin = origin_list[0]
        origin_diff = np.diff(origin_list, axis=0)[0]

        if np.linalg.norm(origin_diff) < 1e-12:
            # Perspective: Same origins, different rays
            plane_normal = np.cross(*ray_list)
        else:
            # Orthographic: Same rays, different origins
            plane_normal = np.cross(ray_list[0], origin_diff)

        plane_normal /= np.linalg.norm(plane_normal)

        for mesh in mesh_elements:
            slices = utils.slice_mesh(mesh, origin, plane_normal)
            for i, vert_slice in enumerate(slices):
                self.lines(vertices=vert_slice,
                           color=mesh.color,
                           name=f'MESHSLICE_{i}_{mesh.name}',
                           extension=mesh.extension,
                           loop=True)

        for block in block_elements:
            slices, values = utils.slice_blocks(block, origin, plane_normal)
            self.blocks(vertices=slices,
                        values=values,
                        vmin=block.vmin,
                        vmax=block.vmax,
                        name=f'BLOCKSLICE_{block.name}',
                        extension=block.extension,
                        block_size=block.block_size,
                        alpha=1.0,
                        )

        # We'll auto-exit the slice mode for now
        self.set_normal_mode()

    def measure_from_rays(self, origin_list: list, ray_list: list) -> None:
        drawables = [m for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        elements = [m.element for m in drawables]

        distances = []

        for mesh in elements:
            points = []
            for i in range(len(origin_list)):
                points.append(utils.mesh_intersection(origin_list[i], ray_list[i], mesh))

            if points[0] is None or points[1] is None:
                continue

            distance = np.linalg.norm(np.diff(points, axis=0))
            distances.append([mesh.id, distance])
            print(f'Distance: {distance} (id: {mesh.id})')

        self.signal_mesh_distances.emit(distances)

    def detect_mesh_intersection(self, x: float, y: float, z: float) -> None:
        ray, origin = self.ray_from_click(x, y, z)
        intersected_ids = []

        drawables = [m for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        elements = [m.element for m in drawables]

        for mesh in elements:
            point = utils.mesh_intersection(origin, ray, mesh)
            # print(f'(Mesh {mesh.id}): Closest intersection: {point}')
            if point is not None:
                intersected_ids.append(mesh.id)

        # Emit signal with clicked mesh
        self.signal_mesh_clicked.emit(intersected_ids)

        # print('-------------------------------')

    """
    Controller
    """
    def set_controller_mode(self, mode: str):
        controllers = {
            'normal': NormalMode,
            'detection': DetectionMode,
            'slice': SliceMode,
            'measurement': MeasurementMode,
        }

        self.current_mode = controllers[mode]()
        self.signal_mode_updated.emit(self.current_mode.name)
        self.update()

    def set_normal_mode(self) -> None:
        self.set_controller_mode('normal')

    def set_detection_mode(self) -> None:
        self.set_controller_mode('detection')

    def set_slice_mode(self) -> None:
        self.set_controller_mode('slice')

    def set_measurement_mode(self) -> None:
        self.set_controller_mode('measurement')

    def perspective_projection(self):
        self.projection_mode = 'perspective'
        self.update()

    def orthographic_projection(self):
        self.projection_mode = 'orthographic'
        self.update()

    # Movement/actions dependent on current mode
    def mouseMoveEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseMoveEvent(event, self)
        self.update()

    def mousePressEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mousePressEvent(event, self)
        self.update()

    def mouseReleaseEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseReleaseEvent(event, self)
        self.update()

    def wheelEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.wheelEvent(event, self)
        self.update()

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs) -> None:
        for url in event.mimeData().urls():
            path = url.toLocalFile()

            if QFileInfo(path).isDir():
                self._load_as_dir(path)
            else:
                self.mesh_by_path(path)

    def _load_as_dir(self, path):
        it = QDirIterator(path, QDirIterator.Subdirectories)
        path_list = []

        while it.hasNext():
            next_path = it.next()
            if QFileInfo(next_path).isFile():
                path_list.append(next_path)

        for path in sorted(path_list):
            self.mesh_by_path(path)
