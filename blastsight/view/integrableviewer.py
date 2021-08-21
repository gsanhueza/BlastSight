#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from OpenGL.GL import *

from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QPoint
from qtpy.QtCore import QTimer
from qtpy.QtCore import Signal
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QPixmap
from qtpy.QtGui import QQuaternion
from qtpy.QtGui import QRegion
from qtpy.QtGui import QVector3D
from qtpy.QtGui import QVector4D
from qtpy.QtWidgets import QOpenGLWidget
from scipy.spatial.transform import Rotation

from .collections.glpostcollection import GLPostCollection
from .collections.glprecollection import GLPreCollection
from .collections.gldrawablecollection import GLDrawableCollection

from .drawables.gldrawable import GLDrawable
from .drawables.blockgl import BlockGL
from .drawables.linegl import LineGL
from .drawables.meshgl import MeshGL
from .drawables.pointgl import PointGL
from .drawables.tubegl import TubeGL
from .drawables.textgl import TextGL

from .drawablefactory import DrawableFactory
from .fpscounter import FPSCounter

from ..controller.basecontroller import BaseController
from ..controller.detectioncontroller import DetectionController
from ..controller.normalcontroller import NormalController
from ..controller.slicecontroller import SliceController
from ..controller.measurementcontroller import MeasurementController

from ..model import utils
from ..model.model import Model


class IntegrableViewer(QOpenGLWidget):
    # Signals
    signal_file_modified = Signal()
    signal_load_success = Signal(int)
    signal_load_failure = Signal()
    signal_export_success = Signal(int)
    signal_export_failure = Signal()

    signal_mesh_distances = Signal(object)
    signal_slice_description = Signal(object)

    signal_mesh_clicked = Signal(object)
    signal_lines_clicked = Signal(object)
    signal_elements_detected = Signal(object)

    signal_process_updated = Signal(int)
    signal_process_started = Signal()
    signal_process_finished = Signal()

    signal_animation_updated = Signal(int)
    signal_animation_started = Signal()
    signal_animation_finished = Signal()

    signal_screen_clicked = Signal(object)
    signal_ray_generated = Signal(object)
    signal_fps_updated = Signal(float)
    signal_controller_updated = Signal(str)
    signal_projection_updated = Signal(str)

    signal_xsection_updated = Signal()
    signal_phantom_updated = Signal()

    signal_camera_rotated = Signal(object)
    signal_camera_translated = Signal(object)
    signal_center_translated = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        # Model
        self.model = Model()

        # Factory
        self.factory = DrawableFactory(self.model)

        # Drawable elements
        self.drawable_collection = GLDrawableCollection()
        self.pre_collection = GLPreCollection()
        self.post_collection = GLPostCollection()

        # Controllers
        self.current_controller = None
        self.controllers = {}

        # Model/View/Projection matrices
        self.model_matrix = QMatrix4x4()
        self.view_matrix = QMatrix4x4()
        self.proj_matrix = QMatrix4x4()

        # FPS Counter
        self.fps_counter = FPSCounter()

        # Initial positions and rotations
        self._rotation_center = np.array([0.0, 0.0, 0.0])
        self._rotation_angle = np.array([0.0, 0.0, 0.0])
        self._camera_position = np.array([0.0, 0.0, 200.0])

        # Cross-section data
        self.last_cross_origin = np.asarray([0.0, 0.0, 0.0])
        self.last_cross_normal = np.asarray([1.0, 0.0, 0.0])
        self.is_cross_sectioned = False
        self.is_phantom_enabled = False

        # Extra information
        self.is_animated = False
        self.fov = 45.0
        self.smoothness = 2.0  # Bigger => smoother (but slower) rotations
        self.current_projection = 'Perspective'  # 'Perspective'/'Orthographic'

        # Initialize viewer
        self.initialize()

    def initialize(self) -> None:
        # Axis/Background/Grid
        self.register_drawable(self.factory.background(id=0), self.pre_collection)
        self.register_drawable(self.factory.axis(id=1), self.post_collection)
        self.register_drawable(self.factory.grid(id=2, visible=False), self.post_collection)
        self.register_drawable(self.factory.lines(id=3, vertices=np.zeros((2, 3)), color=[1.0, 0.8, 0.0],
                                                  visible=False), self.post_collection)

        # Signals
        self.signal_file_modified.connect(self.recreate)
        self.signal_camera_rotated.connect(self.update)
        self.signal_camera_translated.connect(self.update)
        self.signal_center_translated.connect(self.update)

        # Controllers
        self.add_controller(NormalController(self))
        self.add_controller(DetectionController(self))
        self.add_controller(SliceController(self))
        self.add_controller(MeasurementController(self))
        self.set_normal_controller()

        # FPSCounter
        self.fps_counter.add_callback(self.signal_fps_updated.emit)

    """
    Internal methods
    """
    def initializeGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_POINT_SPRITE)
        glDisable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

        # Initialize collections
        self.pre_collection.initialize()
        self.drawable_collection.initialize()
        self.post_collection.initialize()

    def paintGL(self) -> None:
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Propagate uniform values (matrices, viewport, etc)
        self.propagate_uniforms()

        # Draw every GLDrawable (meshes, blocks, points, etc)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.pre_collection.draw()
        self.drawable_collection.draw()
        self.post_collection.draw()

        # Tick FPS counter
        self.fps_counter.tick()

    def resizeGL(self, w: float, h: float) -> None:
        aspect = w / h
        max_distance = 100000.0

        if self.current_projection == 'Perspective':
            self.proj_matrix.perspective(self.fov, aspect, 1.0, max_distance)
        else:  # if self.current_projection == 'Orthographic':
            z = self.off_center[2]
            self.proj_matrix.ortho(-z, z, -z / self.aspect, z / aspect, -max_distance, max_distance)

    @staticmethod
    def setup_model_matrix(matrix: QMatrix4x4, rotation: np.ndarray, translation: np.ndarray) -> None:
        matrix.setToIdentity()

        # Translate matrix (translation = rotation_center)
        matrix.translate(*translation)

        # Rotate matrix
        matrix.rotate(rotation[0], 1.0, 0.0, 0.0)
        matrix.rotate(rotation[1], 0.0, 1.0, 0.0)
        matrix.rotate(rotation[2], 0.0, 0.0, 1.0)

        # Restore matrix
        matrix.translate(*-translation)

    @staticmethod
    def setup_view_matrix(matrix: QMatrix4x4, camera: iter) -> None:
        matrix.setToIdentity()
        matrix.translate(*-camera)

    def propagate_uniforms(self) -> None:
        # Setup matrices
        self.setup_model_matrix(self.model_matrix, self.rotation_angle, self.render_rotation_center)
        self.setup_view_matrix(self.view_matrix, self.render_camera_position)

        # Project (Perspective/Orthographic)
        self.proj_matrix.setToIdentity()
        self.resizeGL(self.width(), self.height())

        # Propagate common uniform values (programs lacking the uniform will ignore the command)
        for collection in [self.pre_collection, self.drawable_collection, self.post_collection]:
            # MVP matrices
            collection.update_uniform('proj_matrix', self.proj_matrix)
            collection.update_uniform('model_view_matrix', self.view_matrix * self.model_matrix)

            # Viewport values (with DPI awareness)
            collection.update_uniform('viewport', *self.viewport)

            # Rendering offset (avoid wobbling when rotating the camera)
            collection.update_uniform('rendering_offset', *self.rendering_offset)

            # Update common uniforms (programs lacking the uniform will ignore the command)
            collection.update_uniform('plane_origin', *self.last_cross_origin)
            collection.update_uniform('plane_normal', *self.last_cross_normal)

    """
    Environment drawables
    """
    @property
    def background(self) -> GLDrawable:
        return self.pre_collection.get(0)

    @property
    def axis(self) -> GLDrawable:
        return self.post_collection.get(1)

    @property
    def grid(self) -> GLDrawable:
        return self.post_collection.get(2)

    @property
    def flatline(self) -> GLDrawable:
        return self.post_collection.get(3)

    """
    Properties
    """
    @property
    def last_id(self) -> int:
        return self.drawable_collection.last_id

    @property
    def last_drawable(self) -> GLDrawable:
        return self.get_drawable(self.last_id)

    @property
    def off_center(self) -> np.ndarray:
        return self.camera_position - self.rotation_center

    @property
    def aspect(self) -> float:
        return 1.0 * self.width() / self.height()

    @property
    def viewport(self) -> iter:
        return [float(self.devicePixelRatio() * self.width()),
                float(self.devicePixelRatio() * self.height())]

    """
    Camera movements/rotations
    """
    @property
    def camera_position(self) -> np.ndarray:
        return self._camera_position

    @property
    def rotation_angle(self) -> np.ndarray:
        return self._rotation_angle

    @property
    def rotation_center(self) -> np.ndarray:
        return self._rotation_center

    @camera_position.setter
    def camera_position(self, value: iter) -> None:
        self._camera_position = np.asarray(value)
        self.signal_camera_translated.emit(value)

    @rotation_angle.setter
    def rotation_angle(self, value: iter) -> None:
        self._rotation_angle = np.asarray(value)
        self.signal_camera_rotated.emit(value)

    @rotation_center.setter
    def rotation_center(self, value: iter) -> None:
        self._rotation_center = np.asarray(value)
        self.signal_center_translated.emit(value)

    """
    Rendering offsets
    """
    @property
    def rendering_offset(self) -> np.ndarray:
        return -self.rotation_center

    @property
    def render_camera_position(self) -> np.ndarray:
        return self.camera_position + self.rendering_offset

    @property
    def render_rotation_center(self) -> np.ndarray:
        return self.rotation_center + self.rendering_offset

    """
    Matrices
    """
    @property
    def model_matrix_math(self) -> QMatrix4x4:
        matrix = QMatrix4x4()
        self.setup_model_matrix(matrix, self.rotation_angle, self.rotation_center)
        return matrix

    @property
    def view_matrix_math(self) -> QMatrix4x4:
        matrix = QMatrix4x4()
        self.setup_view_matrix(matrix, self.camera_position)
        return matrix

    """
    API for partial camera movements/rotations
    """
    def translate(self, x: float, y: float, z: float) -> None:
        self.camera_position += np.array([x, y, z])

    def translate_center(self, x: float, y: float, z: float) -> None:
        self.rotation_center += np.array([x, y, z])

    def rotate(self, alpha: float, beta: float, gamma: float) -> None:
        self.rotation_angle += np.array([alpha, beta, gamma])
        self.rotation_angle %= 360

    """
    API for the camera (animated)
    """
    def get_camera_position(self) -> np.ndarray:
        return self.camera_position

    def get_rotation_center(self) -> np.ndarray:
        return self.rotation_center

    def get_rotation_angle(self) -> np.ndarray:
        return self.rotation_angle

    def set_camera_position(self, target) -> None:
        origin = self.get_camera_position()

        def setter(value):
            self.camera_position = value
        self.animate(origin, target, method=setter) if self.is_animated else setter(target)

    def set_rotation_center(self, target) -> None:
        origin = self.get_rotation_center()

        def setter(value):
            self.rotation_center = value
        self.animate(origin, target, method=setter) if self.is_animated else setter(target)

    def set_rotation_angle(self, target) -> None:
        # Fix any difference > 180° so the camera doesn't over-rotate
        origin = self.get_rotation_angle() % 360
        origin[origin - target > 180] -= 360
        origin[origin - target < -180] += 360

        def setter(value):
            self.rotation_angle = value
        self.animate(origin, target, method=setter) if self.is_animated else setter(target)

    """
    Animation / Turbo
    """
    def set_turbo_rendering(self, status: bool) -> None:
        self.blockSignals(True)

        for d in self.get_all_drawables():
            d.is_boostable = status

        self.blockSignals(False)
        self.recreate()

    def set_animated(self, status: bool) -> None:
        self.is_animated = status

    def animate(self, start, end, method: callable, **kwargs) -> callable:
        milliseconds = int(kwargs.get('milliseconds', 300))
        steps = int(kwargs.get('steps', 20))

        timer = QTimer(self)
        linspace = iter(np.linspace(start, end, steps))
        counter = []

        def start_animation():
            timer.start(milliseconds / steps)
            self.signal_animation_started.emit()

        def update_animation():
            try:
                method(next(linspace))
                self.update()

                counter.append(None)
                self.signal_animation_updated.emit(100.0 * len(counter) / steps)
            except StopIteration:
                end_animation()

        def end_animation():
            timer.stop()
            self.signal_animation_finished.emit()

        timer.timeout.connect(update_animation)
        start_animation()

    """
    Projections
    """
    def perspective_projection(self) -> None:
        self.current_projection = 'Perspective'
        self.signal_projection_updated.emit(self.current_projection)
        self.resizeGL(self.width(), self.height())
        self.update()

    def orthographic_projection(self) -> None:
        self.current_projection = 'Orthographic'
        self.signal_projection_updated.emit(self.current_projection)
        self.resizeGL(self.width(), self.height())
        self.update()

    """
    Registration methods
    """
    def register_drawable(self, drawable, collection=None):
        if drawable is None:
            self.signal_load_failure.emit()
            return None

        if collection is None:
            collection = self.drawable_collection

        # Update shared settings
        drawable.is_cross_sectioned = self.is_cross_sectioned

        # Register in collection
        drawable.add_observer(self)
        collection.add(drawable)

        # Emit success signals
        self.signal_file_modified.emit()
        self.signal_load_success.emit(drawable.id)

        return drawable

    """
    Load methods by arguments
    """
    def mesh(self, *args, **kwargs) -> MeshGL:
        return self.register_drawable(self.factory.mesh(*args, **kwargs))

    def blocks(self, *args, **kwargs) -> BlockGL:
        return self.register_drawable(self.factory.blocks(*args, **kwargs))

    def points(self, *args, **kwargs) -> PointGL:
        return self.register_drawable(self.factory.points(*args, **kwargs))

    def lines(self, *args, **kwargs) -> LineGL:
        return self.register_drawable(self.factory.lines(*args, **kwargs))

    def tubes(self, *args, **kwargs) -> TubeGL:
        return self.register_drawable(self.factory.tubes(*args, **kwargs))

    def text(self, *args, **kwargs) -> TextGL:
        return self.register_drawable(self.factory.text(*args, **kwargs))

    """
    Load methods by path
    """
    def load_mesh(self, path: str, *args, **kwargs) -> MeshGL:
        return self.register_drawable(self.factory.load_mesh(path, *args, **kwargs))

    def load_blocks(self, path: str, *args, **kwargs) -> BlockGL:
        return self.register_drawable(self.factory.load_blocks(path, *args, **kwargs))

    def load_points(self, path: str, *args, **kwargs) -> PointGL:
        return self.register_drawable(self.factory.load_points(path, *args, **kwargs))

    def load_lines(self, path: str, *args, **kwargs) -> LineGL:
        return self.register_drawable(self.factory.load_lines(path, *args, **kwargs))

    def load_tubes(self, path: str, *args, **kwargs) -> TubeGL:
        return self.register_drawable(self.factory.load_tubes(path, *args, **kwargs))

    def load_mesh_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_mesh, *args, **kwargs)

    def load_blocks_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_blocks, *args, **kwargs)

    def load_points_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_points, *args, **kwargs)

    def load_lines_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_lines, *args, **kwargs)

    def load_tubes_folder(self, path: str, *args, **kwargs) -> list:
        return self.load_folder(path, self.load_tubes, *args, **kwargs)

    """
    Generalized loaders
    """
    def load_folder(self, path: str, loader: callable, *args, **kwargs) -> list:
        return self.load_multiple(self.model.get_paths_from_directory(path), loader, *args, **kwargs)

    def load_multiple(self, path_list: list, loader: callable, *args, **kwargs) -> list:
        # Do not process if loading an empty path list
        if len(path_list) == 0:
            return []

        self.signal_process_started.emit()
        loaded = []

        for i, path in enumerate(path_list, 1):
            # Block only loaded signals
            self.blockSignals(True)
            drawable = loader(path, *args, **kwargs)
            self.blockSignals(False)

            if drawable is not None:
                loaded.append(drawable)

            self.signal_process_updated.emit(int(100 * i / len(path_list)))

        # Emit signals depending on results
        if len(loaded) > 0:
            self.signal_file_modified.emit()
            self.signal_load_success.emit(self.last_id)
        else:
            self.signal_load_failure.emit()

        self.signal_process_finished.emit()

        return loaded

    """
    Export methods
    """
    def export_element(self, path: str, _id: int) -> None:
        try:
            self.model.export(path, _id)
            self.signal_export_success.emit(_id)
        except Exception:
            self.signal_export_failure.emit()

    """
    Drawable manipulation
    """
    def get_drawable(self, _id: int):
        return self.drawable_collection.get(_id)

    def show_drawable(self, _id: int) -> None:
        self.get_drawable(_id).show()

    def hide_drawable(self, _id: int) -> None:
        self.get_drawable(_id).hide()

    def update_drawable(self, _id: int) -> None:
        self.makeCurrent()
        self.get_drawable(_id).reload()
        self.recreate()

    def delete(self, _id: int) -> None:
        if _id < 0:
            return

        self.makeCurrent()
        self.model.delete(_id)
        self.drawable_collection.delete(_id)
        self.signal_file_modified.emit()

    def update_all(self) -> None:
        self.makeCurrent()
        for _id in self.get_all_ids():
            self.get_drawable(_id).reload()
        self.recreate()

    def clear(self) -> None:
        self.makeCurrent()
        self.model.clear()
        self.drawable_collection.clear()
        self.signal_file_modified.emit()

    def recreate(self) -> None:
        self.pre_collection.recreate()
        self.drawable_collection.recreate()
        self.post_collection.recreate()
        self.update()

    """
    Drawable retrieval
    """
    def get_all_ids(self) -> list:
        return self.drawable_collection.all_ids()

    def get_all_drawables(self) -> list:
        return self.drawable_collection.all_drawables()

    def get_all_meshes(self) -> list:
        return self.drawable_collection.select(MeshGL)

    def get_all_blocks(self) -> list:
        return self.drawable_collection.select(BlockGL)

    def get_all_points(self) -> list:
        return self.drawable_collection.select(PointGL)

    def get_all_lines(self) -> list:
        return self.drawable_collection.select(LineGL)

    def get_all_tubes(self) -> list:
        return self.drawable_collection.select(TubeGL)

    """
    Camera handling
    """
    def camera_at(self, _id: int) -> None:
        self.fit_to_bounds(*self.get_drawable(_id).bounding_box)

    def plan_view(self) -> None:
        self.set_rotation_angle([0.0, 0.0, 0.0])

    def north_view(self) -> None:
        self.set_rotation_angle([270.0, 0.0, 270.0])

    def east_view(self) -> None:
        self.set_rotation_angle([270.0, 0.0, 0.0])

    def fit_to_bounds(self, min_bound: np.ndarray, max_bound: np.ndarray) -> None:
        center = (min_bound + max_bound) / 2
        self.rotation_center = center

        # Put the camera in a position that allow us to see between the boundaries.
        md = np.max(np.diff([min_bound, max_bound], axis=0))
        fov_rad = self.fov * np.pi / 180.0

        # In perspective projection, we need a clever trigonometric calculation.
        if self.current_projection == 'Perspective':
            dist = (md / np.tan(fov_rad / 2) + md) / 2.0
            z_shift = dist * max(1.0, 1.0 / self.aspect)

        # But in orthographic projection, it's more direct.
        else:
            dist = md / 2
            z_shift = dist * max(1.0, self.aspect)

        camera_shift = center + np.array([0.0, 0.0, 1.1 * z_shift])
        self.set_camera_position(camera_shift)
        self.update()

    def fit_to_screen(self) -> None:
        bounds = self.bounding_box()

        if bounds is not None:
            self.fit_to_bounds(*bounds)

    def bounding_box(self) -> tuple or None:
        drawables = list(filter(lambda d: d.is_visible, self.get_all_drawables()))

        if len(drawables) == 0:
            return None

        min_all = np.inf * np.ones(3)
        max_all = -np.inf * np.ones(3)

        for drawable in drawables:
            min_bound, max_bound = drawable.bounding_box
            min_all = np.min((min_all, min_bound), axis=0)
            max_all = np.max((max_all, max_bound), axis=0)

        return min_all, max_all

    """
    Utilities
    """
    def get_pixmap(self) -> QPixmap:
        pixmap = QPixmap(self.size())
        self.render(pixmap, QPoint(), QRegion(self.rect()))
        return pixmap

    def take_screenshot(self, save_path: str) -> None:
        if bool(save_path):
            self.get_pixmap().save(save_path)

    def screen_to_ndc(self, x: float, y: float, z: float) -> np.ndarray:
        # Click at bottom-left of screen => (-1.0, -1.0, z)
        # Click at top-right of screen => (1.0, 1.0, z)
        # But we can't really know where's z, so we just return 1.0
        return np.array([
            (2.0 * x / self.width()) - 1.0,
            1.0 - (2.0 * y / self.height()),
            1.0])

    def unproject(self, x: float, y: float, z: float) -> np.ndarray:
        # Adapted from http://antongerdelan.net/opengl/raycasting.html
        # Note: x, y, z must be normalized to [-1.0, +1.0]

        # We'd use `QVector4D(x, y, -1.0, 1.0)`, but PySide2
        # hasn't implemented QMatrix4x4 * QVector4D yet.
        vector = [x, y, -1.0, 1.0]
        temp_matrix = QMatrix4x4(*[e for e in vector for _ in range(4)])

        ray_eye = (self.proj_matrix.inverted()[0] * temp_matrix).column(0)
        ray_eye = QVector4D(ray_eye.x(), ray_eye.y(), -1.0, 0.0)

        # We'd use `ray_eye`, but PySide2
        # hasn't implemented QMatrix4x4 * QVector4D yet.
        vector = [ray_eye.x(), ray_eye.y(), ray_eye.z(), ray_eye.w()]
        temp_matrix = QMatrix4x4(*[e for e in vector for _ in range(4)])

        # Our self.view_matrix and self.model_matrix are altered to simplify rendering.
        # For ray calculations, that's irrelevant, although we'll still use the correct ones for consistency.
        ray_world = ((self.view_matrix_math * self.model_matrix_math).inverted()[0] * temp_matrix).column(0).toVector3D()
        ray = ray_world.normalized()
        return np.array([ray.x(), ray.y(), ray.z()])

    def ray_from_click(self, x: float, y: float, z: float) -> np.ndarray:
        # Perspective projection is straightforward
        if self.current_projection == 'Perspective':
            return self.unproject(*self.screen_to_ndc(x, y, z))

        # Orthographic projection "forces" a click in the center (normalized to [-1.0, +1.0])
        return self.unproject(0.0, 0.0, 0.0)

    def origin_from_click(self, x: float, y: float, z: float) -> np.ndarray:
        # Perspective projection is straightforward
        def perspective_origin() -> np.ndarray:
            origin = (self.view_matrix * self.model_matrix).inverted()[0].column(3).toVector3D()

            # Remember that we have a rendering offset now!
            return np.array([origin.x(), origin.y(), origin.z()]) - self.rendering_offset

        # Orthographic projection needs a bit more of vector arithmetic.
        # A click in the center of the screen gives us the perfect ray,
        # by recycling the perspective's un-project method.

        # But if we don't click in the exact center of screen,
        # we need to trick the origin calculation.
        def orthographic_origin() -> np.ndarray:
            ndc = self.screen_to_ndc(x, y, z)
            aspect_bias = np.array([1.0, 1.0 / self.aspect, 0.0])

            # The idea is to strategically move the camera by an offset, so that
            # clicking anywhere in the screen will give us the same result as
            # clicking at the exact center of the screen from a shifted camera.
            offset = self.off_center[2] * ndc * aspect_bias

            # Hack to get the origin when the click is not exactly at center of screen.
            self.view_matrix.translate(*-offset)
            origin = perspective_origin()
            self.view_matrix.translate(*offset)

            return origin

        if self.current_projection == 'Perspective':
            return perspective_origin()

        return orthographic_origin()

    def get_normal(self, origin_list, ray_list: list) -> np.ndarray:
        # Perspective: Same origins, different rays
        if self.current_projection == 'Perspective':
            return utils.normalize(np.cross(*ray_list))

        # Orthographic: Same rays, different origins
        origin_diff = np.diff(origin_list, axis=0)[0]
        return utils.normalize(np.cross(ray_list[0], origin_diff))

    @staticmethod
    def angles_from_vectors(normal: np.ndarray, up: np.ndarray) -> np.ndarray:
        # Returns a list of angles that allows the normal to look directly at the camera
        # Extrinsic: xyz / Intrinsic: XYZ (Tait-Bryan angles)
        # In self.paintGL, we're currently using the XYZ intrinsic rotation order.

        rotmat = QQuaternion.fromDirection(QVector3D(*normal), QVector3D(*up)).toRotationMatrix().data()
        return Rotation.from_matrix(np.array(rotmat).reshape((3, 3))).as_euler('XYZ', degrees=True)

    def set_camera_from_vectors(self, normal: np.ndarray, up: np.ndarray, as_axis: bool = True) -> None:
        # Auto-moves the camera using the normal as direction

        def best_projection() -> np.ndarray:
            # We will alter the 'up' vector, projecting it onto each of the axes.
            # The longest projection will be used instead of the 'up' vector.
            candidates = np.identity(3)
            lengths = np.abs(utils.dot_by_row(candidates, np.tile(up, (3, 1))))
            return utils.normalize(candidates[np.argmax(lengths)])

        if as_axis:
            # For now, we'll use the best Z projection
            # If the dot-product fails (highly improbable), we'll use the Y projection.
            if np.dot([0.0, 0.0, 1.0], up) > 1e-6:
                up = np.array([0.0, 0.0, 1.0])
            else:
                up = np.array([0.0, 1.0, 0.0])

        self.set_rotation_angle(self.angles_from_vectors(normal, up))

    def generate_slice_description(self, origin_list: list, ray_list: list) -> dict:
        # A plane is created from `origin` and `ray_list`.
        # In perspective projection, the origin is the same.
        origin = origin_list[0]
        normal = self.get_normal(origin_list, ray_list)
        up = utils.normalize(np.cross(ray_list[0], normal))

        response = {
            'origin': origin,
            'normal': normal,
            'up': up,
        }

        # Emit description of the slice
        self.signal_slice_description.emit(response)

        return response

    def slice_meshes(self, origin: np.ndarray, normal: np.ndarray, include_hidden: bool = False) -> list:
        # By default, slice only visible meshes
        meshes = list(filter(lambda m: m.is_visible or include_hidden, self.get_all_meshes()))

        return self.model.slice_meshes(origin, normal, meshes)

    def slice_blocks(self, origin: np.ndarray, normal: np.ndarray, include_hidden: bool = True) -> list:
        # By default, slice visible and hidden blocks
        blocks = list(filter(lambda m: m.is_visible or include_hidden, self.get_all_blocks()))

        return self.model.slice_blocks(origin, normal, blocks)

    def slice_points(self, origin: np.ndarray, normal: np.ndarray, include_hidden: bool = True) -> list:
        # By default, slice visible and hidden points
        points = list(filter(lambda m: m.is_visible or include_hidden, self.get_all_points()))

        return self.model.slice_points(origin, normal, points)

    def intersect_meshes(self, origin: np.ndarray, ray: np.ndarray, include_hidden: bool = False) -> list:
        # By default, intersect only visible meshes
        meshes = list(filter(lambda m: m.is_visible or include_hidden, self.get_all_meshes()))

        return self.model.intersect_meshes(origin, ray, meshes)

    def intersect_lines(self, origin: np.ndarray, ray: np.ndarray, include_hidden: bool = False) -> list:
        # By default, intersect only visible lines
        lines = list(filter(lambda m: m.is_visible or include_hidden, self.get_all_lines()))

        return self.model.intersect_lines(origin, ray, lines)

    def intersect_elements(self, origin: np.ndarray, ray: np.ndarray, include_hidden: bool = False) -> list:
        meshes = self.intersect_meshes(origin, ray, include_hidden)
        lines = self.intersect_lines(origin, ray, include_hidden)
        results = meshes + lines

        self.signal_mesh_clicked.emit(meshes)
        self.signal_lines_clicked.emit(lines)
        self.signal_elements_detected.emit(results)

        return results

    def measure_from_rays(self, origin_list: list, ray_list: list) -> dict:
        meshes = list(filter(lambda m: m.is_visible, self.get_all_meshes()))

        response = self.model.measure_from_rays(origin_list, ray_list, meshes)
        self.signal_mesh_distances.emit(response)

        return response

    def cross_section(self, origin: np.ndarray, normal: np.ndarray) -> None:
        # Uniforms in cross-section are always auto-updated in self.paintGL()
        self.last_cross_origin = np.asarray(origin)
        self.last_cross_normal = np.asarray(normal)
        self.signal_xsection_updated.emit()

        self.update()

    def set_cross_section(self, status: bool) -> None:
        self.is_cross_sectioned = status

        for m in self.get_all_meshes() + self.get_all_blocks():
            m.is_cross_sectioned = status

        self.signal_xsection_updated.emit()

    def set_phantom(self, status: bool) -> None:
        self.is_phantom_enabled = status

        for m in self.get_all_meshes():
            m.is_phantom = status

        self.signal_phantom_updated.emit()

    """
    Controller
    """
    def add_controller(self, controller: BaseController) -> None:
        self.controllers[controller.name] = controller

    def set_controller(self, name: str) -> None:
        self.current_controller = self.controllers.get(name)
        self.signal_controller_updated.emit(name)
        self.update()

    def set_normal_controller(self) -> None:
        self.set_controller('Normal')

    def set_detection_controller(self) -> None:
        self.set_controller('Detection')

    def set_slice_controller(self) -> None:
        self.set_controller('Slice')

    def set_measurement_controller(self) -> None:
        self.set_controller('Measurement')

    """
    Events (dependent on current controller)
    """
    def mouseMoveEvent(self, event, *args, **kwargs) -> None:
        self.current_controller.mouseMoveEvent(event)
        self.update()

    def mousePressEvent(self, event, *args, **kwargs) -> None:
        self.current_controller.mousePressEvent(event)
        self.update()

    def mouseDoubleClickEvent(self, event, *args, **kwargs) -> None:
        self.current_controller.mouseDoubleClickEvent(event)
        self.update()

    def mouseReleaseEvent(self, event, *args, **kwargs) -> None:
        self.current_controller.mouseReleaseEvent(event)
        self.update()

    def keyPressEvent(self, event, *args, **kwargs) -> None:
        self.current_controller.keyPressEvent(event)
        self.update()

    def keyReleaseEvent(self, event, *args, **kwargs) -> None:
        self.current_controller.keyReleaseEvent(event)
        self.update()

    def wheelEvent(self, event, *args, **kwargs) -> None:
        self.current_controller.wheelEvent(event)
        self.update()

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs) -> None:
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if QFileInfo(path).isDir():
                self.load_folder(path, self.load_mesh)
            else:
                self.load_mesh(path)
